from roboid import *

hamster = Hamster()
hamster.wheels(50, 50)
wait(500)

hamster.wheels(-50, -50)
wait(500)

hamster.stop()
