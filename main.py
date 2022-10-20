
import random

class RexZombie:
    def __init__(self, vomit_ready=True, hp=136, exhaustion=0):
        self.vomit_ready = vomit_ready
        self.hp = hp
        self.exhaustion=exhaustion
        self.dead = False

    def __str__(self):
        return f"R: {self.hp}/136,{self.exhaustion}/5, {self.vomit_ready}"


class Zombie:
    def __init__(self):
        self.hp = 22
        self.exhaustion=0
        self.dead = False

    def __str__(self):
        return f"Z: {self.hp}/136,{self.exhaustion}/5"

def get_sickening_damage():
    return random.randint(1, 10) + random.randint(1, 10) + random.randint(1, 10) + random.randint(1, 10)


def does_pass_con_save():
    return random.randint(1, 20)+3 >= 19


def does_zombie_survive_with_1(dmg):
    return random.randint(1, 20) + 3 >= dmg+5


def is_space_in_room(zombies, rexes, new_rexes):
    return len(zombies) + len(rexes) + len(new_rexes) < 100


def does_rex_keep_vomit():
    return random.randint(1, 6) != 1


def run_simulation():
    corpses = 0
    zombies = [Zombie(), Zombie(), Zombie(), Zombie()]
    rexes = [RexZombie(True, 65), RexZombie(True, 74, 1), RexZombie(True, 88), RexZombie(True, 109),
             RexZombie(True, 62, 1), RexZombie(True, 102), RexZombie(True, 29, 1), ]

    for turn in range(2, 60):
        # print(f"**** simulating turn {turn+1} **** ")
        for zombie in zombies:
            if not does_pass_con_save():
                dmg = get_sickening_damage()
                zombie.hp -= dmg
                zombie.exhaustion += 1
                if zombie.exhaustion >= 5:
                    # print("zombie died of exhaustion")
                    zombie.dead = True
                    corpses += 1
                    continue
                if zombie.hp <= 0:
                    if does_zombie_survive_with_1(dmg):
                        zombie.hp = 1
                    else:
                        # print("zombie died")
                        zombie.dead = True
                        replacement_rex = RexZombie(exhaustion=zombie.exhaustion)
                        rexes.append(replacement_rex)
                        # print(f"Rex size: {len(rexes)}. Added {replacement_rex}")

        zombies = [tup for tup in zombies if not tup.dead]

        new_rexes = []
        for rex in rexes:
            if not does_pass_con_save():
                dmg = get_sickening_damage()
                rex.hp -= dmg
                if rex.exhaustion >= 5:
                    # print("Rex died of exhaustion")
                    rex.dead = True
                    corpses += 1
                    continue
                if rex.hp <= 0:
                    if does_zombie_survive_with_1(dmg):
                        rex.hp = 1
                    else:
                        # print("Rex died")
                        rex.dead = True
                        corpses += 1
                        continue

            if is_space_in_room(zombies, rexes, new_rexes):
                if rex.vomit_ready:
                    rex.vomit_ready = does_rex_keep_vomit()
                    if not rex.vomit_ready:
                        # print("rex can not vomit again")
                        pass
                    # print("Rex made new zombie")
                    new_zombie = Zombie()
                    if not does_pass_con_save():
                        dmg = get_sickening_damage()
                        new_zombie.hp -= dmg
                        new_zombie.exhaustion += 1
                        if zombie.hp <= 0:
                            if does_zombie_survive_with_1(dmg):
                                zombie.hp = 1
                            else:
                                # print("newly created zombie died immediately")
                                replacement_rex = RexZombie(exhaustion=new_zombie.exhaustion)
                                new_rexes.append(replacement_rex)
                                # print(f"Rex size: {len(rexes)}. New rexes: {len(new_rexes)}. Added {replacement_rex}")
                        else:
                            zombies.append(new_zombie)
            else:
                # print("No more room!")
                pass
        rexes.extend(new_rexes)
        rexes = [tup for tup in rexes if not tup.dead]

        #print(f"*** ending turn with {len(zombies)} zombies and {len(rexes)} rexes")
    return len(zombies), len(rexes), corpses

if __name__ == '__main__':
    for _ in range(100):
        zombies, rexes, corpses = run_simulation()
        print(f"*** ending simulation with {zombies} zombies and {rexes} rexes. The room is filled with {corpses} corpses")
        if zombies+rexes == 0:
            print("THE ROOM DID NOT FILL!")

