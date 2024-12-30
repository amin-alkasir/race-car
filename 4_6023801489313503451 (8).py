import numpy as np

class Car:
    def __init__(self):
        self.position = 0
    
    def refuel(self):
        self.fuel = self.fuel_capacity
    
    def refuel_needed(self,time):
        fuel = self.fuel - self.dm_dt * time
        if fuel < self.fuel_capacity * 0.15:
            return (True,self.fuel_capacity-self.fuel)
        return (False,0)

    def step(self, time, time_step):
        self.fuel = self.fuel - self.dm_dt * time
        if self.fuel == 0:
            return
        mass0 = self.m0 + self.fuel_capacity
        mass = self.m0 + self.fuel
        velocity = self.ve * np.log(mass0 / mass)
        self.velocity_vec.append(velocity)
        self.position = np.cumsum(np.array(self.velocity_vec) * time_step)[-1]
        print(f'{self.name}, {self.position}')

    @staticmethod
    def random_car(i):
        car = Car()
        car.fuel_capacity = 10000
        car.fuel = car.fuel_capacity
        car.m0 = np.random.random() * 10000 + 20000
        car.dm_dt = np.random.random() * 8 + 2
        car.ve = 3000
        car.velocity_vec = []
        car.name = f'car_{i}'
        car.refuel_count_down = 0
        car.mass = car.m0 + car.fuel_capacity
        return car


class Race:
    def __init__(self):
        self.time_step = 0.1
        self.race_distance = 1000
        self.refuel_per_car = 3
        self.gas_station_positions = [
            self.race_distance/4,
            self.race_distance*2/4,
            self.race_distance*3/4,
        ]
        
        def is_near_gas_station(p):
            for sp in self.gas_station_positions:
                if p >= sp - 20 and p <= sp + 20:
                    return True
            return False
        
        cars = [
            Car.random_car(1),
            Car.random_car(2),
            Car.random_car(3),
            Car.random_car(4)
        ]
        t = 0
        finished = False
        while True:
            for car in cars:
                refuel_needed = car.refuel_needed(t)
                if is_near_gas_station(car.position) and refuel_needed[0]:
                    car.refuel_count_down = int(refuel_needed[1])
                    car.refuel()
                elif car.refuel_count_down > 0:
                    car.refuel_count_down -= 1
                else:
                    car.step(t,self.time_step)

                if car.position >= self.race_distance:
                    print(f'{car.name} Won! in time {t}')
                    finished = True
                    break  
            t += self.time_step    
            if finished:
                break  
    

def main():
    Race()

if __name__ == "__main__":
    main()