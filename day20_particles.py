"""
https://adventofcode.com/2017/day/20

1-D case first

claim: if |a_0| > |a_1| then there exists a t after which
particle 0 is closer to the origin than particle 1.

proof: say particle a_i has
position x_i(t) and
velocity v_i(t) and
acceleration a_i (which is constant)

then v_i(t) = v_0 + a_i * t
and  x_i(t) = x_0 + v_0 * t + .5 * a_i * t^2

in particular:

x_0(t) = x_0 + v_0 * t + .5 * a_0 * t^2
x_1(t) = x_1 + v_1 * t + .5 * a_1 * t^2

and as t gets really, really big, this behaves like
.5 * a_i * t^2, and so the bigger a_i is further away

==

now in n dimensions, the same thing is true in each dimension
in particular, in 3 dimension, we have that

<x, y, z> ~ 0.5 * t^2 * <a_x, a_y, a_z>
"""
from typing import NamedTuple, Dict, List
from collections import defaultdict

class XYZ(NamedTuple):
    x: int
    y: int
    z: int

    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

class Particle(NamedTuple):
    position: XYZ
    velocity: XYZ
    acceleration: XYZ

def parse_triple(triple: str) -> XYZ:
    """
    a triple is like p=<1, 2, 3>
    """
    x, y, z = triple[2:].strip().replace('<', '').replace('>', '').split(',')
    return XYZ(int(x), int(y), int(z))

assert parse_triple("p=<1, -2, 3>") == XYZ(1, -2, 3)

def parse_line(line: str) -> Particle:
    p, v, a = line.strip().split(", ")
    return Particle(position=parse_triple(p),
                    velocity=parse_triple(v),
                    acceleration=parse_triple(a))

assert parse_line("p=<-317,1413,1507>, v=<19,-102,-108>, a=<1,-3,-3>") == \
    Particle(XYZ(-317, 1413, 1507), XYZ(19, -102, -108), XYZ(1, -3, -3))

def step(particle: Particle) -> Particle:
    position = particle.position
    velocity = particle.velocity
    acceleration = particle.acceleration

    new_velocity = XYZ(velocity.x + acceleration.x,
                       velocity.y + acceleration.y,
                       velocity.z + acceleration.z)
    new_position = XYZ(position.x + new_velocity.x,
                       position.y + new_velocity.y,
                       position.z + new_velocity.z)

    return Particle(new_position, new_velocity, acceleration)

assert step(Particle(XYZ(-317, 1413, 1507), XYZ(19, -102, -108), XYZ(1, -3, -3))) == \
    Particle(XYZ(-297, 1308, 1396), XYZ(20, -105, -111), XYZ(1, -3, -3))

def remove_collisions(particles: List[Particle]) -> List[Particle]:
    position_counts: Dict[XYZ, int] = defaultdict(int)
    for particle in particles:
        position_counts[particle.position] += 1

    return [particle for particle in particles
            if position_counts[particle.position] == 1]

TEST_PARTICLES = [
    Particle(XYZ(-317, 1413, 1507), XYZ(19, -102, -108), XYZ(1, -3, -32)),
    Particle(XYZ(-317, -1413, 150), XYZ(190, -12, -108), XYZ(1, -30, -3)),
    Particle(XYZ(-317, 1413, 1507), XYZ(19, -2, -18), XYZ(10, -3, -3))
]

assert remove_collisions(TEST_PARTICLES) == [
    Particle(XYZ(-317, -1413, 150), XYZ(190, -12, -108), XYZ(1, -30, -3))
]

if __name__ == "__main__":
    with open('day20_input.txt') as f:
        lines = f.read().split("\n")
    particles = [parse_line(line) for line in lines if line.strip()]
    print(min(enumerate(particles), key=lambda pair: pair[1].acceleration.manhattan()))

    # this number was picked arbitrarily and we just ran it and saw that the
    # number of particles stopped going down. this is not principled in the slightest
    # and we feel very bad about ourselves.
    for i in range(10000):
        particles = remove_collisions(particles)
        particles = [step(particle) for particle in particles]
        print(i, len(particles))
