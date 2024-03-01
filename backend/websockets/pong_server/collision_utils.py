from class_vec2 import Vec2

def OnSegment(p, q, r):
    if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
        q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
        return True
    return False

def Orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # collinear
    return 1 if val > 0 else 2  # clock or counterclockwise

def DoIntersect(p1, q1, p2, q2):
    o1 = Orientation(p1, q1, p2)
    o2 = Orientation(p1, q1, q2)
    o3 = Orientation(p2, q2, p1)
    o4 = Orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and OnSegment(p1, p2, q1):
        return True

    if o2 == 0 and OnSegment(p1, q2, q1):
        return True

    if o3 == 0 and OnSegment(p2, p1, q2):
        return True

    if o4 == 0 and OnSegment(p2, q1, q2):
        return True

    return False  # Doesn't fall in any cases

def PaddleInterceptionPoint(ball, paddle, last_ball_pos):
    i = Vec2(paddle.position.x, 0.0)
    t = abs((i.x - last_ball_pos.x) / (ball.position.x - last_ball_pos.x))
    i.y = last_ball_pos.y * (1.0 - t) + ball.position.y * t
    return i