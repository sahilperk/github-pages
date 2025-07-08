#!/usr/bin/env python3
"""
Park Runner Simulation
A comprehensive simulation of a person running in the park.
"""

import time
import random
import math
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional


class Weather:
    """Represents weather conditions in the park."""
    
    def __init__(self):
        self.conditions = ["sunny", "cloudy", "light rain", "windy", "overcast"]
        self.current_condition = random.choice(self.conditions)
        self.temperature = random.randint(15, 30)  # Celsius
        self.humidity = random.randint(40, 80)  # Percentage
    
    def update_weather(self):
        """Randomly update weather conditions."""
        if random.random() < 0.1:  # 10% chance of weather change
            self.current_condition = random.choice(self.conditions)
            self.temperature += random.randint(-2, 2)
            self.temperature = max(10, min(35, self.temperature))
    
    def get_weather_description(self) -> str:
        """Get a formatted weather description."""
        return f"{self.current_condition.title()}, {self.temperature}°C, {self.humidity}% humidity"
    
    def affects_running(self) -> float:
        """Return a multiplier for running performance based on weather."""
        multiplier = 1.0
        if self.current_condition == "light rain":
            multiplier *= 0.9  # Slightly slower
        elif self.current_condition == "windy":
            multiplier *= 0.95
        elif self.temperature > 28:
            multiplier *= 0.85  # Hot weather slows down
        elif self.temperature < 18:
            multiplier *= 1.05  # Cool weather is better for running
        return multiplier


class Park:
    """Represents the park environment with various features."""
    
    def __init__(self, name: str = "Central Park"):
        self.name = name
        self.size_hectares = random.randint(50, 200)
        self.trails = self._generate_trails()
        self.features = self._generate_features()
        self.weather = Weather()
        self.time_of_day = "morning"
        self.crowd_level = random.choice(["empty", "light", "moderate", "busy"])
    
    def _generate_trails(self) -> List[Dict]:
        """Generate different running trails in the park."""
        trails = [
            {"name": "Main Loop", "distance_km": 3.2, "difficulty": "easy", "surface": "paved"},
            {"name": "Forest Trail", "distance_km": 2.8, "difficulty": "moderate", "surface": "dirt"},
            {"name": "Hill Challenge", "distance_km": 4.1, "difficulty": "hard", "surface": "mixed"},
            {"name": "Lakeside Path", "distance_km": 2.5, "difficulty": "easy", "surface": "paved"},
            {"name": "Scenic Route", "distance_km": 5.0, "difficulty": "moderate", "surface": "gravel"}
        ]
        return random.sample(trails, k=random.randint(3, 5))
    
    def _generate_features(self) -> List[str]:
        """Generate park features."""
        possible_features = [
            "duck pond", "playground", "rose garden", "picnic area", 
            "exercise stations", "benches", "water fountain", "restrooms",
            "bike rental", "food truck", "monument", "amphitheater"
        ]
        return random.sample(possible_features, k=random.randint(4, 8))
    
    def get_trail_by_name(self, name: str) -> Optional[Dict]:
        """Get a trail by its name."""
        for trail in self.trails:
            if trail["name"].lower() == name.lower():
                return trail
        return None
    
    def update_environment(self):
        """Update park environment conditions."""
        self.weather.update_weather()
        
        # Update time of day
        times = ["early morning", "morning", "midday", "afternoon", "evening"]
        current_index = times.index(self.time_of_day) if self.time_of_day in times else 1
        if random.random() < 0.2:  # 20% chance of time progression
            self.time_of_day = times[min(current_index + 1, len(times) - 1)]
        
        # Update crowd level based on time
        if self.time_of_day in ["morning", "evening"]:
            self.crowd_level = random.choice(["light", "moderate", "busy"])
        elif self.time_of_day == "midday":
            self.crowd_level = random.choice(["empty", "light", "moderate"])
        else:
            self.crowd_level = random.choice(["empty", "light"])


class Runner:
    """Represents a person running in the park."""
    
    def __init__(self, name: str, fitness_level: str = "average"):
        self.name = name
        self.fitness_level = fitness_level  # beginner, average, good, excellent
        self.energy = 100
        self.max_energy = 100
        self.total_distance = 0.0
        self.current_speed = 0.0  # km/h
        self.pace_per_km = timedelta(minutes=6)  # Default 6 min/km
        self.is_running = False
        self.current_trail = None
        self.position_on_trail = 0.0  # km from start
        self.running_time = timedelta()
        self.breaks_taken = 0
        self.hydration_level = 100
        self.mood = "energetic"
        self.achievements = []
        
        self._set_fitness_attributes()
    
    def _set_fitness_attributes(self):
        """Set attributes based on fitness level."""
        fitness_multipliers = {
            "beginner": {"speed": 0.7, "endurance": 0.6, "recovery": 0.8},
            "average": {"speed": 1.0, "endurance": 1.0, "recovery": 1.0},
            "good": {"speed": 1.3, "endurance": 1.4, "recovery": 1.2},
            "excellent": {"speed": 1.6, "endurance": 1.8, "recovery": 1.5}
        }
        
        multiplier = fitness_multipliers.get(self.fitness_level, fitness_multipliers["average"])
        
        # Base pace is 6 min/km, adjust based on fitness
        base_minutes = 6.0 / multiplier["speed"]
        self.pace_per_km = timedelta(minutes=base_minutes)
        self.max_energy = int(80 + (20 * multiplier["endurance"]))
        self.energy = self.max_energy
    
    def start_running(self, trail: Dict, park: Park):
        """Start running on a specific trail."""
        if self.is_running:
            return f"{self.name} is already running!"
        
        if self.energy < 20:
            return f"{self.name} is too tired to run. Take a break first!"
        
        self.is_running = True
        self.current_trail = trail
        self.position_on_trail = 0.0
        
        # Calculate speed based on trail difficulty and weather
        base_speed = 60 / self.pace_per_km.total_seconds() * 60  # km/h
        
        difficulty_multipliers = {"easy": 1.0, "moderate": 0.9, "hard": 0.8}
        difficulty_mult = difficulty_multipliers.get(trail["difficulty"], 1.0)
        
        weather_mult = park.weather.affects_running()
        
        self.current_speed = base_speed * difficulty_mult * weather_mult
        
        return f"{self.name} starts running on {trail['name']} at {self.current_speed:.1f} km/h!"
    
    def run_step(self, park: Park, duration_minutes: float = 1.0) -> List[str]:
        """Simulate one step of running (default 1 minute)."""
        if not self.is_running:
            return [f"{self.name} is not currently running."]
        
        events = []
        
        # Calculate distance covered in this step
        distance_step = (self.current_speed / 60) * duration_minutes
        self.position_on_trail += distance_step
        self.total_distance += distance_step
        self.running_time += timedelta(minutes=duration_minutes)
        
        # Energy consumption
        energy_cost = self._calculate_energy_cost(duration_minutes, park)
        self.energy = max(0, self.energy - energy_cost)
        
        # Hydration decrease
        self.hydration_level = max(0, self.hydration_level - random.uniform(0.5, 2.0))
        
        # Check if completed the trail
        if self.position_on_trail >= self.current_trail["distance_km"]:
            events.append(f"🏁 {self.name} completed {self.current_trail['name']}!")
            self._check_achievements()
            self.position_on_trail = 0.0
            if self.energy > 30 and random.random() < 0.7:
                events.append(f"{self.name} decides to run another lap!")
            else:
                self.stop_running()
                events.append(f"{self.name} stops running after completing the trail.")
        
        # Random events
        events.extend(self._generate_random_events(park))
        
        # Update mood based on current state
        self._update_mood()
        
        # Check if runner needs to stop due to exhaustion
        if self.energy <= 0:
            self.stop_running()
            events.append(f"💨 {self.name} is exhausted and stops running.")
        
        return events
    
    def _calculate_energy_cost(self, duration_minutes: float, park: Park) -> float:
        """Calculate energy cost for running duration."""
        base_cost = duration_minutes * 2
        
        # Adjust for trail difficulty
        difficulty_multipliers = {"easy": 1.0, "moderate": 1.3, "hard": 1.6}
        difficulty_mult = difficulty_multipliers.get(self.current_trail["difficulty"], 1.0)
        
        # Adjust for weather
        weather_mult = 1.0
        if park.weather.temperature > 25:
            weather_mult += 0.3
        if park.weather.current_condition == "light rain":
            weather_mult += 0.1
        
        # Adjust for hydration
        if self.hydration_level < 30:
            weather_mult += 0.4
        
        return base_cost * difficulty_mult * weather_mult
    
    def _generate_random_events(self, park: Park) -> List[str]:
        """Generate random events during running."""
        events = []
        
        if random.random() < 0.1:  # 10% chance per minute
            event_type = random.choice([
                "wildlife", "people", "scenery", "challenge", "discovery"
            ])
            
            if event_type == "wildlife":
                animals = ["squirrels", "ducks", "joggers with dogs", "cyclists", "birds"]
                animal = random.choice(animals)
                events.append(f"🐿️ {self.name} sees {animal} along the trail.")
            
            elif event_type == "people":
                interactions = [
                    "waves at another runner",
                    "says 'good morning' to a walker",
                    "high-fives a fellow jogger",
                    "encourages a struggling runner"
                ]
                events.append(f"👋 {self.name} {random.choice(interactions)}.")
            
            elif event_type == "scenery":
                sights = [
                    "admires the blooming flowers",
                    "enjoys the view of the lake",
                    "appreciates the morning sunlight",
                    "notices new graffiti art"
                ]
                events.append(f"🌸 {self.name} {random.choice(sights)}.")
            
            elif event_type == "challenge":
                if self.energy > 50:
                    events.append(f"💪 {self.name} pushes harder up a steep hill!")
                    self.current_speed *= 1.2
                
            elif event_type == "discovery":
                if random.choice(park.features) == "water fountain":
                    events.append(f"💧 {self.name} stops for a quick drink at the water fountain.")
                    self.hydration_level = min(100, self.hydration_level + 20)
        
        return events
    
    def _update_mood(self):
        """Update runner's mood based on current state."""
        if self.energy > 70 and self.hydration_level > 60:
            self.mood = "energetic"
        elif self.energy > 40:
            self.mood = "steady"
        elif self.energy > 20:
            self.mood = "tired"
        else:
            self.mood = "exhausted"
    
    def _check_achievements(self):
        """Check for running achievements."""
        # Distance achievements
        if self.total_distance >= 5 and "First 5K" not in self.achievements:
            self.achievements.append("First 5K")
        elif self.total_distance >= 10 and "10K Runner" not in self.achievements:
            self.achievements.append("10K Runner")
        
        # Speed achievements
        if self.current_speed > 12 and "Speed Demon" not in self.achievements:
            self.achievements.append("Speed Demon")
        
        # Endurance achievements
        if self.running_time.total_seconds() > 3600 and "Hour Runner" not in self.achievements:
            self.achievements.append("Hour Runner")
    
    def take_break(self, duration_minutes: int = 5):
        """Take a break to recover energy."""
        if self.is_running:
            self.stop_running()
        
        recovery = min(20, duration_minutes * 2)
        self.energy = min(self.max_energy, self.energy + recovery)
        self.hydration_level = min(100, self.hydration_level + 10)
        self.breaks_taken += 1
        
        return f"{self.name} takes a {duration_minutes}-minute break and recovers {recovery} energy."
    
    def stop_running(self):
        """Stop running."""
        self.is_running = False
        self.current_speed = 0.0
        return f"{self.name} stops running."
    
    def get_status(self) -> Dict:
        """Get current runner status."""
        return {
            "name": self.name,
            "fitness_level": self.fitness_level,
            "is_running": self.is_running,
            "energy": f"{self.energy}/{self.max_energy}",
            "hydration": f"{self.hydration_level}%",
            "mood": self.mood,
            "total_distance": f"{self.total_distance:.2f} km",
            "current_speed": f"{self.current_speed:.1f} km/h" if self.is_running else "0 km/h",
            "running_time": str(self.running_time).split('.')[0],
            "current_trail": self.current_trail["name"] if self.current_trail else "None",
            "position_on_trail": f"{self.position_on_trail:.2f} km" if self.is_running else "N/A",
            "achievements": self.achievements
        }


class ParkRunningSimulation:
    """Main simulation class that orchestrates the park running experience."""
    
    def __init__(self):
        self.park = Park()
        self.runner = None
        self.simulation_time = 0  # minutes elapsed
        self.events_log = []
    
    def create_runner(self, name: str, fitness_level: str = "average") -> str:
        """Create a new runner."""
        self.runner = Runner(name, fitness_level)
        message = f"Created runner: {name} (Fitness: {fitness_level})"
        self.events_log.append(message)
        return message
    
    def show_park_info(self) -> str:
        """Display park information."""
        info = f"\n🏞️  {self.park.name}\n"
        info += f"📏 Size: {self.park.size_hectares} hectares\n"
        info += f"🌤️  Weather: {self.park.weather.get_weather_description()}\n"
        info += f"🕐 Time: {self.park.time_of_day.title()}\n"
        info += f"👥 Crowd Level: {self.park.crowd_level.title()}\n\n"
        
        info += "🛤️  Available Trails:\n"
        for i, trail in enumerate(self.park.trails, 1):
            info += f"  {i}. {trail['name']} - {trail['distance_km']} km "
            info += f"({trail['difficulty']}, {trail['surface']})\n"
        
        info += f"\n🎯 Park Features: {', '.join(self.park.features)}\n"
        
        return info
    
    def start_run(self, trail_name: str) -> str:
        """Start running on a specific trail."""
        if not self.runner:
            return "No runner created. Create a runner first!"
        
        trail = self.park.get_trail_by_name(trail_name)
        if not trail:
            available = [t["name"] for t in self.park.trails]
            return f"Trail '{trail_name}' not found. Available trails: {', '.join(available)}"
        
        result = self.runner.start_running(trail, self.park)
        self.events_log.append(result)
        return result
    
    def simulate_step(self, duration_minutes: float = 1.0) -> List[str]:
        """Simulate one time step."""
        if not self.runner:
            return ["No runner created. Create a runner first!"]
        
        self.simulation_time += duration_minutes
        
        # Update park environment occasionally
        if self.simulation_time % 10 == 0:  # Every 10 minutes
            self.park.update_environment()
        
        events = []
        
        if self.runner.is_running:
            events = self.runner.run_step(self.park, duration_minutes)
        else:
            events = [f"{self.runner.name} is taking a break in the park."]
        
        self.events_log.extend(events)
        return events
    
    def get_simulation_status(self) -> str:
        """Get current simulation status."""
        if not self.runner:
            return "No runner created."
        
        status = self.runner.get_status()
        
        info = f"\n👟 Runner Status:\n"
        info += f"Name: {status['name']} ({status['mood']})\n"
        info += f"Energy: {status['energy']} | Hydration: {status['hydration']}\n"
        info += f"Total Distance: {status['total_distance']}\n"
        info += f"Running Time: {status['running_time']}\n"
        info += f"Current Speed: {status['current_speed']}\n"
        
        if status['current_trail'] != "None":
            info += f"Current Trail: {status['current_trail']}\n"
            info += f"Position: {status['position_on_trail']}\n"
        
        if status['achievements']:
            info += f"🏆 Achievements: {', '.join(status['achievements'])}\n"
        
        info += f"\n⏰ Simulation Time: {self.simulation_time} minutes\n"
        info += f"🌤️  Current Weather: {self.park.weather.get_weather_description()}\n"
        
        return info
    
    def run_automatic_simulation(self, duration_minutes: int = 30):
        """Run an automatic simulation for a specified duration."""
        if not self.runner:
            return "No runner created. Create a runner first!"
        
        print(f"\n🏃‍♂️ Starting {duration_minutes}-minute automatic simulation...\n")
        
        # Auto-select a trail if not running
        if not self.runner.is_running:
            trail = random.choice(self.park.trails)
            self.start_run(trail["name"])
        
        for minute in range(duration_minutes):
            events = self.simulate_step(1.0)
            
            # Print significant events
            for event in events:
                if any(emoji in event for emoji in ["🏁", "💨", "🏆", "💧", "💪"]):
                    print(f"Minute {minute + 1}: {event}")
            
            # Take breaks automatically if energy is low
            if self.runner.energy < 20 and not self.runner.is_running:
                break_msg = self.runner.take_break()
                print(f"Minute {minute + 1}: {break_msg}")
            
            # Restart running if energy is recovered and not currently running
            elif (self.runner.energy > 40 and not self.runner.is_running and 
                  self.simulation_time % 5 == 0):  # Check every 5 minutes
                trail = random.choice(self.park.trails)
                restart_msg = self.start_run(trail["name"])
                print(f"Minute {minute + 1}: {restart_msg}")
            
            time.sleep(0.1)  # Small delay for visualization
        
        print(f"\n✅ Simulation completed!")
        print(self.get_simulation_status())


def main():
    """Main function to run the park running simulation."""
    simulation = ParkRunningSimulation()
    
    print("🏃‍♂️ Welcome to the Park Running Simulation! 🏃‍♀️")
    print("=" * 50)
    
    # Create a runner
    runner_name = input("Enter runner's name (or press Enter for 'Alex'): ").strip()
    if not runner_name:
        runner_name = "Alex"
    
    fitness_levels = ["beginner", "average", "good", "excellent"]
    print(f"\nFitness levels: {', '.join(fitness_levels)}")
    fitness = input("Enter fitness level (or press Enter for 'average'): ").strip().lower()
    if fitness not in fitness_levels:
        fitness = "average"
    
    simulation.create_runner(runner_name, fitness)
    
    print(simulation.show_park_info())
    
    while True:
        print("\n" + "=" * 50)
        print("Available commands:")
        print("1. 'run [trail_name]' - Start running on a trail")
        print("2. 'step [minutes]' - Simulate time step (default 1 minute)")
        print("3. 'status' - Show current status")
        print("4. 'break [minutes]' - Take a break (default 5 minutes)")
        print("5. 'auto [minutes]' - Run automatic simulation (default 30 minutes)")
        print("6. 'park' - Show park information")
        print("7. 'quit' - Exit simulation")
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == "quit":
            print("Thanks for running! 🏃‍♂️💨")
            break
        elif command == "status":
            print(simulation.get_simulation_status())
        elif command == "park":
            print(simulation.show_park_info())
        elif command.startswith("run "):
            trail_name = command[4:].strip()
            print(simulation.start_run(trail_name))
        elif command.startswith("step"):
            parts = command.split()
            duration = float(parts[1]) if len(parts) > 1 else 1.0
            events = simulation.simulate_step(duration)
            for event in events:
                print(event)
        elif command.startswith("break"):
            parts = command.split()
            duration = int(parts[1]) if len(parts) > 1 else 5
            print(simulation.runner.take_break(duration))
        elif command.startswith("auto"):
            parts = command.split()
            duration = int(parts[1]) if len(parts) > 1 else 30
            simulation.run_automatic_simulation(duration)
        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()