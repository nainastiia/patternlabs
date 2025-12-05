class DroneController:
    def __init__(self, implementor):
        self.impl = implementor#Зберігає посилання на об'єкт імплементатора

    def goto(self, coord):
        self.impl.move_to(coord)#викликає move_to

    def adjust_course(self, vector):
        self.impl.adjust_course(vector)

    def set_swarm(self):
        self.impl.set_mode("swarm")

    def set_single(self):
        self.impl.set_mode("single")