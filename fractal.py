import sys  # importing sys, so I can run it via. cmd
# from swampy.TurtleWorld import *  # importing the TurtleWorld if you prefer to use this
from FractalWorld import *  # importing the Fractalworld module


class Rule(object):
    def __init__(self, left, right):
        """An object with left and right side"""
        self.right = right
        self.left = left

    def __str__(self):
        return '%s ->%s' % (self.left, self.right)

    def apply_rule(self, list):
        """applying the rule"""
        list = [self.right if x==self.left else x for x in list]
        return list


class cmd(object):
    """command object with name, command and argument"""
    def __init__(self, command, argument):
        self.command = command
        self.argument = argument

    def __str__(self):
        return '%s, %s' % (self.command, self.argument)


class fractal(object):
    """
    start, cmd_list, rule_list, depth, length
    """
    rule_list = []
    cmd_mapping = {}

world = FractalWorld(width=700,height=500,delay=0)
bob = Fractal(draw=False)

"""
if you want to use the TurtleWorld you can uncomment this, and comment the FractalWorld out

world = TurtleWorld() #creating the world
bob = Turtle() #defining my turtle, we name him Bob
bob.delay=0.0 #setting the delay
"""

pu(bob)  # placing the turtle
bk(bob, -400)
rt(bob)
bk(bob, -300)
lt(bob)
pd(bob)

# fin=open("test2.fdl")
# fin=open("koch.fdl")
# fin=open("sierpinski.fdl")
fin = open("sierpinski2.fdl")
# fin=open("dragon.fdl") #choosing a file to open
# fin=open("fern.fdl")
# fin=open(sys.argv[1]) #opens the file passed in cmd as first argument
# fin=open("tree.fdl")


def apply_command(cmd_to_apply):  # applying the command
    if cmd_to_apply.command == "nop":  # defining no operation
        return
    elif cmd_to_apply.command == "scale":  # defining scale
        fractal.length = float(fractal.length)*float(cmd_to_apply.argument)
    elif cmd_to_apply.argument is None:  # defining fd object with length
        eval(cmd_to_apply.command)(bob, fractal.length)
    else:
        eval(cmd_to_apply.command)(bob, int(cmd_to_apply.argument))  # defining the other commands


def apply_rules(depth):  # applying rules
    x = 0
    while depth > x:
        if depth == 0:  # return list as it is
            return
        if depth == 1:  # apply rules once
            fractal.start = fractal.rule_list[0].apply_rule(fractal.start)
            fractal.start = [val for sublist in fractal.start for val in sublist]  # flatten the list
            return
        for i in range(len(fractal.rule_list)):  # if there is more than one rule, apply them one at a time.
            fractal.start = fractal.rule_list[i].apply_rule(fractal.start)
        fractal.start = [val for sublist in fractal.start for val in sublist]  # flatten the list
        x = x + 1

for line in fin:  # opening file
    word = line.strip()  # stripping
    if line.startswith("start"):
        fractal.start = word.replace("start", " ").strip().split()  # giving start the value from start
    if line.startswith("rule"):  # isolating the rules
        word = word.split("->")
        right = word[1].split()  # defining the right side
        left = word[0].replace("rule", " ").strip()  # defining the left side
        current_rule = Rule(left, right)  # making the rule object
        fractal.rule_list.append(current_rule)   # appending the current rule to the rule list
    if line.startswith("length"):  # isolating the length
        length = word.replace("length", " ").strip()
        fractal.length = float(length)  # setting the length
    if line.startswith("depth"):  # isolating the depth
        fractal.depth = int(word.replace("depth", " ").strip())  # setting the depth

    if line.startswith("cmd"):  # isolating the cmds
        word = word.replace("cmd ", " ").strip()
        word = word.split()
        name = word[0]  # setting the name eg F
        command = word[1]  # setting the command eg fd
        if len(word) == 3:
            argument = word[2]  # setting the argument if there is one
        else:
            argument = None  # else set it to none.
        current_cmd = cmd(command, argument)  # making a cmd object
        fractal.cmd_mapping[name] = current_cmd  # mapping the current_cmd to the name

apply_rules(fractal.depth)

for element in fractal.start:  # applying the commands to every element in list of letters
    if element in fractal.cmd_mapping:
        apply_command(fractal.cmd_mapping[element])

wait_for_user()