# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from random import shuffle, random
# Create your models here.

class Game(models.Model):
    phase = models.CharField(max_length=255, default="draw")
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Hadron(models.Model):
    num_quarks = models.IntegerField(default=1)
    position = models.IntegerField(default=-1)
    location = models.CharField(max_length=10, default="beam")
    game = models.ForeignKey(Game, related_name="hadrons")

class Quark(models.Model):
    COLORS = [
        "red",
        "green",
        "blue"
    ]
    # no "top" quarks in the base game
    FLAVORS = [
        "up",
        "down",
        "charm",
        "strange",
        "bottom"
    ]
    color = models.CharField(max_length=5, default=COLORS[0])
    flavor = models.CharField(max_length=7, default=FLAVORS[0])
    anti = models.BooleanField(default=False)
    is_annihilator = models.BooleanField(default=False)
    hadron = models.ForeignKey(Hadron, related_name="quarks")

class GameLogic(object):
    def __init__(self, user):
        self.deck = []
        if hasattr(user, "game"):
            self.game = user.game
            cards = Hadron.objects.filter(game=self.game, location="deck").order_by("position")
            for card in cards:
                self.deck.append(card.id)
        else:
            self.game = Game.objects.create(player=user)
            for c in Quark.COLORS:
                for f in Quark.FLAVORS:
                    h = Hadron.objects.create(game=self.game)
                    q = Quark.objects.create(hadron=h)
                    self.deck.append(h.id)
            shuffle(self.deck)
            for hid in self.deck:
                q = Hadron.objects.get(id=hid).quarks.first()
                q.anti = True
                q.save()
            shuffle(self.deck)
            self.save_deck_order()
    def save_deck_order(self):
        for i in range(len(self.deck)):
            h = Hadron.objects.get(id=self.deck[i])
            h.position = i
            h.save()
    def draw(self):
        hid = self.deck.pop()
        h = Hadron.objects.get(id=hid)
        h.location = "beam"
        h.save()
        return h
    def discard(self, qid):
        q = Quark.objects.get(id=qid)
        h = Hadron.objects.get(quarks__contains=q, game=self.game)
        h.location = "discard"
        h.save()
    def shuffle(self):
        cards = Hadron.objects.filter(location="discard", game=self.game)
        for h in cards:
            q = h.quarks.first()
            q.anti = not q.anti
            q.save()
            h.location = "deck"
            h.save()
            self.deck.append(h.id)
        new_h = Hadron.objects.create(game=self.game)
        new_a = Quark.objects.create(hadron=new_h, is_annihilator=True)
        self.deck.append(new_h)
        shuffle(self.deck)
        self.save_deck_order()