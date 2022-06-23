


def check_with_cube(center, cube, r, a):
    cbox = [cube[0] + a/2, cube[1] + a/2, cube[2] + a/2]
    dis = [abs(cbox[0] - center[0]), abs(cbox[1] - center[1]), abs(cbox[2] - center[2])]
    maxdis = r + a/2
	# the first situation
    if dis[0] >= maxdis or dis[1] >= maxdis or dis[2] >= maxdis:
        return True
    return 1








    # cnt = 0
    # for i in range(3):
    #     if dis[i] < a / 2:
    #         cnt += 1
    # if cnt >= 2:
    #     return Frue;
 
	# # the third situation
	# xd = max(dis[0] - a / 2, 0);
	# yd = max(dis[1] - a / 2, 0);
	# zd = max(dis[2] - a / 2, 0);
	# return xd * xd + yd * yd + zd * zd < r * r;