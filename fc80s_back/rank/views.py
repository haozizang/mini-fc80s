from django.shortcuts import render
import json
from django.http import HttpResponse, Http404
from django.template import loader
from django.db.models import Q

from datetime import datetime
import pytz

from index.models import Activity, Player, Match, Team

def rank(request):
    # turn hex kanji into string
    body_str = str(request.body, encoding = "utf8")
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    print("body", body_str)
    return HttpResponse(json.dumps("rank view function"), content_type="application/json")

def upload(request):
    # turn hex kanji into string
    body_str = str(request.body, encoding = "utf8")
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    print("body", body_str)
    activity_timestamp = body["activity_time"]
    # get local time-zone
    time_zone = datetime.utcnow().astimezone().tzinfo
    print(time_zone)
    time = datetime.fromtimestamp(float(activity_timestamp)/1000, time_zone)
    print("backend time:", time)
    # TODO: 应用新的 Activity 模型
    activity, if_created = Activity.objects.get_or_create(act_time = time)
    print("if_created: ", if_created)
    # when activity is not created, don't insert the teams neither
    if if_created:
        for team in body["teams"]:
            print("team", team)
            # create team in DB
            team = Team.objects.create(name = team["name"], rank = team["rank"], activity = activity, win = team["win"], draw = team["draw"], loss = team["loss"], point = team["point"], goal = team["goal"])
    return HttpResponse(json.dumps({"if_create": if_created}), content_type="application/json")

# return the rank of latest activity
def getRank(request):
    # turn hex kanji into string
    body_str = str(request.body, encoding = "utf8")
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    print("body", body_str)
    print("path", request.path)
    print("Method", request.method)
    # get or create the player for the sender
    player, if_created = Player.objects.get_or_create(open_id=body["open_id"], defaults={'name': body["nick_name"], 'open_id': body["open_id"]})
    print("player.name: ", player.name)
    print("if created: ", if_created)
    match_num = 0
    team_num = 0
    if not if_created:
        # get club the player belongs
        club = Club.objects.filter(name=player.name)
        if club:
            print("player", player.name, "belongs to club: ", club.name)
        # not new user => check team and match
        # get all the team(activity) the sender get involved
        team_list = Team.objects.filter(players__open_id=body["open_id"])
        team_num = team_list.count()
        # get all the matches the sender's in
        for team in team_list:
            print('team name: ', team.name)
            home_match_list = Match.objects.filter(home_team__id=team.id)
            away_match_list = Match.objects.filter(away_team__id=team.id)
            print("home match num: ", home_match_list.count())
            print("away match num: ", away_match_list.count())
            match_num += home_match_list.count()
            match_num += away_match_list.count()
            print("match count: ", match_num)
        print("team num(activity num): ", team_list.count())
    resp = {
        'activities': team_num,
        'matches': match_num,
        'offence': player.offence,
        'defence': player.defence,
        'stability': player.stability,
        'teamwork': player.teamwork,
        'passion': player.passion,
        'win_ratio': player.win_ratio
    }

    return HttpResponse(json.dumps({"if_create": if_created}), content_type="application/json")

