from django.db import models

# player
class Player(models.Model):
    # openID -> id
    name = models.CharField(max_length=30)
    open_id = models.CharField(max_length=50, null=True)
    offence = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stability = models.IntegerField(default=0)
    teamwork = models.IntegerField(default=0)
    passion = models.IntegerField(default=0)
    win_ratio = models.IntegerField(default=0)

    # 此函数决定 模型对象访问显示(Player.objects.all()) 和 admin 站点显示
    def __str__(self):
        return self.name

# class Activity(models.Model):
#     time = models.DateTimeField()

class Team(models.Model):
    name = models.CharField(max_length=30)
    captain = models.ForeignKey(Player, related_name="captain", on_delete=models.SET_NULL, blank=True, null=True)
    time = models.DateTimeField()
    players = models.ManyToManyField(Player)
    rank = models.IntegerField(null=True)
    # win = models.IntegerField(default=0)
    # draw = models.IntegerField(default=1)
    # loss = models.IntegerField(default=0)
    # 添加GS(goal scored), GA(goal against) -> 算出 GD(goal difference)

    def __str__(self):
        return self.name

class Match(models.Model):
    # home_team = models.CharField(max_length=30)
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.SET_NULL, blank=True, null=True)
    # away_team = models.CharField(max_length=30)
    away_team = models.ForeignKey(Team, related_name="away_name", on_delete=models.SET_NULL, blank=True, null=True)
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
    time = models.DateTimeField()

    def __str__(self):
        return self.home_team.name + str(self.home_goals) + " : " + str(self.away_goals) + self.away_team.name
