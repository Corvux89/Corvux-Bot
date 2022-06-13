from CorvuxBot.contants import *


def is_admin(ctx):
    return ctx.author.id in ADMIN_USERS

