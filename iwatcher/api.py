from flask import Blueprint, g, request, jsonify
from peewee import *
from iwatcher.models import Camera, UCcheck,TimePoint

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/get', methods=('POST',))
def get_cams():
    geo = request.get_json()

    west = ((float)(geo['w']))*1000000
    east = ((float)(geo['e']))*1000000
    north = ((float)(geo['n']))*1000000
    south = ((float)(geo['s']))*1000000

    cams = (Camera.select(
        Camera.id,
        Camera.lat,
        Camera.lon,
        Camera.dev
    ).where(
        (Camera.lon >= west) & (Camera.lon <= east) & (Camera.lat <= north) & (Camera.lat >= south)) )

    cams_arr = []
    for cam_dict in cams.dicts().iterator():
        elem = cam_dict.copy()
        elem['lat'] = elem['lat']/1000000
        elem['lon'] = elem['lon']/1000000
        cams_arr.append(elem.copy())
    return jsonify(cams_arr)


@bp.route('/add', methods=('POST',))
def add_cam():
    user = g.user
    cams_arr = []
    if user:
        if user.is_active:
            add_req = request.get_json()
            cam, created = Camera.get_or_create(
                lat = 1000000*(float)(add_req['lat']),
                lon = 1000000*(float)(add_req['lon']),
                dev = (int)(add_req['dev']),
                author = user,
                about = add_req['about'])
            tp = TimePoint.create(author=user)

            cams_arr.append({
                'id': cam.id,
                'lat': add_req['lat'],
                'lon': add_req['lon'],
                'dev': add_req['dev']
            })
    return jsonify(cams_arr)


@bp.route('/rate/<id>', methods=('POST',))
def rate_cam(id):
    user = g.user
    cam_arr = []
    if user:
        cam = Camera.get_or_none(Camera.id == id)
        if cam:
            if cam.author != user:
                check, newc = UCcheck.get_or_create(user=user, camera=cam)

            q = (UCcheck.select(fn.Count(UCcheck.camera).alias('rating'))
                .where(UCcheck.camera == cam)
                .dicts())
            for line in q:
                cam_arr.append(line.copy())
                cam_arr[0]['id'] = cam.id
    return jsonify(cam_arr)


@bp.route('/info/<id>', methods=('POST',))
def cam_info(id):
    if request.method == 'POST':
        cam_info = {}
        q = (Camera.select(
                Camera.id,
                Camera.added,
                Camera.about,
                fn.Count(UCcheck.user).alias('rating'))
            .join(UCcheck, JOIN.LEFT_OUTER)
            .where(Camera.id == id)
            .dicts())
        for line in q:
            cam_info = line
            cam_info['added'] = line['added'].strftime('%d %b %Y')
        return jsonify(line)
