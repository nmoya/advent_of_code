from enum import Enum
from functools import cache, partial
from typing import Callable, Dict, List, Tuple

from tqdm import tqdm

import utils


class Mappings(Enum):
    seeds = "seeds:"
    seed_to_soil = "seed-to-soil map:"
    soil_to_fertilizer = "soil-to-fertilizer map:"
    fertilizer_to_water = "fertilizer-to-water map:"
    water_to_light = "water-to-light map:"
    light_to_temperature = "light-to-temperature map:"
    temperature_to_humidity = "temperature-to-humidity map:"
    humidity_to_location = "humidity-to-location map:"


class Almanac:
    def __init__(
        self,
        seeds: List[int],
        seed_to_soil: List[Callable],
        soil_to_fertilizer: List[Callable],
        fertilizer_to_water: List[Callable],
        water_to_light: List[Callable],
        light_to_temperature: List[Callable],
        temperature_to_humidity: List[Callable],
        humidity_to_location: List[Callable],
    ):
        self.seeds = seeds
        self.seed_to_soil = seed_to_soil
        self.soil_to_fertilizer = soil_to_fertilizer
        self.fertilizer_to_water = fertilizer_to_water
        self.water_to_light = water_to_light
        self.light_to_temperature = light_to_temperature
        self.temperature_to_humidity = temperature_to_humidity
        self.humidity_to_location = humidity_to_location

    @staticmethod
    def find_relevant_lines(lines, section: Mappings) -> Tuple[int, int]:
        if section == Mappings.seeds:
            return 0, 1
        start, end = None, None
        for i, line in enumerate(lines):
            if line.startswith(section.value):
                start = i + 1
            elif start is not None and line == "":
                end = i
                break
        if start is not None and end is None:
            end = len(lines)
        if start is None or end is None:
            raise Exception(f"Could not find section {section.value}")

        return start, end

    @staticmethod
    def parse_correlation(all_lines: List[str], section: Mappings) -> Dict[int, int]:
        start, end = Almanac.find_relevant_lines(all_lines, section)
        lines = all_lines[start:end]
        out = []
        for line in lines:
            raw_dest_start, raw_source_start, raw_length = Almanac.parse_number_line(line)

            def get_value(dest_start, source_start, length, value: int) -> int:
                offset = source_start - dest_start
                if source_start <= value < source_start + length:
                    return value - offset
                return None

            out.append(partial(get_value, raw_dest_start, raw_source_start, raw_length))
        return out

    @staticmethod
    def parse_number_line(line: str) -> List[int]:
        return [int(seed) for seed in line.strip().split(" ")]

    @staticmethod
    def parse_seeds(all_lines: List[str], section: Mappings):
        start, end = Almanac.find_relevant_lines(all_lines, section)
        line = all_lines[start:end][0]
        return Almanac.parse_number_line(line.replace("seeds:", ""))

    @staticmethod
    def parse_input(text: str):
        lines = text.split("\n")
        return Almanac(
            seeds=Almanac.parse_seeds(lines, Mappings.seeds),
            seed_to_soil=Almanac.parse_correlation(lines, Mappings.seed_to_soil),
            soil_to_fertilizer=Almanac.parse_correlation(lines, Mappings.soil_to_fertilizer),
            fertilizer_to_water=Almanac.parse_correlation(lines, Mappings.fertilizer_to_water),
            water_to_light=Almanac.parse_correlation(lines, Mappings.water_to_light),
            light_to_temperature=Almanac.parse_correlation(lines, Mappings.light_to_temperature),
            temperature_to_humidity=Almanac.parse_correlation(lines, Mappings.temperature_to_humidity),
            humidity_to_location=Almanac.parse_correlation(lines, Mappings.humidity_to_location),
        )

    def find_applicable_rule(self, value: int, predicates) -> int:
        for predicate in predicates:
            if predicate(value) is not None:
                return predicate(value)
        return value

    def find_location(self, seed: int) -> int:
        soil = self.find_applicable_rule(seed, self.seed_to_soil)
        fertilizer = self.find_applicable_rule(soil, self.soil_to_fertilizer)
        water = self.find_applicable_rule(fertilizer, self.fertilizer_to_water)
        light = self.find_applicable_rule(water, self.water_to_light)
        temperature = self.find_applicable_rule(light, self.light_to_temperature)
        humidity = self.find_applicable_rule(temperature, self.temperature_to_humidity)
        location = self.find_applicable_rule(humidity, self.humidity_to_location)
        return location

    def find_lowest_location(self) -> int:
        return min(self.find_location(seed) for seed in self.seeds)

    def find_lowest_location_seed_range(self) -> int:
        even = [seed for i, seed in enumerate(self.seeds) if i % 2 == 0]
        odd = [seed for i, seed in enumerate(self.seeds) if i % 2 == 1]
        min_so_far = float("inf")
        for seed_start, seed_end in tqdm(zip(even, odd)):
            for seed in tqdm(range(seed_start, seed_start + seed_end)):
                # print(seed, self.find_location(seed))
                min_so_far = min(min_so_far, self.find_location(seed))
        return min_so_far


def seed_fertilizer(filename):
    almanac = Almanac.parse_input(utils.read_input(filename))
    print(almanac.find_lowest_location())
    print(almanac.find_lowest_location_seed_range())


def test_samples():
    text = utils.read_input("src/2023_5_seed_fertilizer_sample.txt")
    sample = text.split("\n")
    assert Almanac.find_relevant_lines(sample, Mappings.seeds) == (0, 1)
    assert Almanac.find_relevant_lines(sample, Mappings.seed_to_soil) == (3, 5)
    assert Almanac.find_relevant_lines(sample, Mappings.soil_to_fertilizer) == (7, 10)
    assert Almanac.find_relevant_lines(sample, Mappings.fertilizer_to_water) == (12, 16)
    assert Almanac.find_relevant_lines(sample, Mappings.water_to_light) == (18, 20)
    assert Almanac.find_relevant_lines(sample, Mappings.light_to_temperature) == (22, 25)
    assert Almanac.find_relevant_lines(sample, Mappings.temperature_to_humidity) == (27, 29)
    assert Almanac.find_relevant_lines(sample, Mappings.humidity_to_location) == (31, 33)

    a = Almanac.parse_input(text)
    assert a.find_location(82) == 46
    assert len(Almanac.parse_correlation(sample, Mappings.seed_to_soil)) == 2


if __name__ == "__main__":
    test_samples()
    seed_fertilizer("src/2023_5_seed_fertilizer.txt")
