from os import write
import re, csv
from collections import OrderedDict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class AdventureParser:

    skill_pattern = re.compile(r"\bDC\s+(\b\d+\b)\s+\b(Strength|Dexterity|Constitution|Wisdom|Intelligence|Charisma)\s+\((.+?)\)")
    save_pattern = re.compile(r"\bDC\s+(\b\d+\b)\s+\b(Strength|Dexterity|Constitution|Wisdom|Intelligence|Charisma)\s+?saving throw\b")

    def __init__(self, rootdir, adventure_name, write_data=True):
        self.adventure_name = adventure_name
        self.rootdir = rootdir
        self.skill_checks = []
        self.saving_throws = []
        self.skill_data = {}
        self.save_data = {}
        self.find_skill_checks()
        self.find_saving_throws()
        self.skill_data = self.prepare_data(self.skill_checks)
        self.save_data = self.prepare_data(self.saving_throws)
        if write_data:
            self.write_skills()
            self.write_saves()
            self.write_save_totals()
            self.write_skill_check_data()

    def find_skill_checks(self):
        text = ""
        with open("%s%s.txt" % (self.rootdir, self.adventure_name), "r", encoding="utf-8") as textfile:
            text = ' '.join(textfile.readlines()).replace('\n', '')
        for match in self.skill_pattern.finditer(text):
            d = {
                'DC': int(match.group(1)),
                'Ability': match.group(2),
            }
            try:
                d['Skill'] = match.group(3)
            except IndexError:
                d['Skill'] = None
            self.skill_checks.append(d)

    def find_saving_throws(self):
        text = ""
        with open("%s%s.txt" % (self.rootdir, self.adventure_name), "r", encoding="utf-8") as textfile:
            text = ' '.join(textfile.readlines()).replace('\n', '')
        for match in self.save_pattern.finditer(text):
            d = {
                'DC': int(match.group(1)),
                'Ability': match.group(2),
            }
            self.saving_throws.append(d)
    
    def prepare_data(self, data):
        dc_set = sorted(list(set([item['DC'] for item in data])))
        ability_set = sorted(list(set([item['Ability'] for item in data])))

        dc_count = {}
        for dc in dc_set:
            dc_count[dc] = [item['DC'] for item in data].count(dc)

        ability_count = {}
        for ability in ability_set:
            ability_count[ability] = [item['Ability'] for item in data].count(ability)

        ability_data = {}
        for ability in ability_set:
            ability_data[ability] = [item['DC'] for item in data if item['Ability'] == ability]
        
        return {
            'dc_set': dc_set,
            'ability_set': ability_set,
            'dc_count': dc_count, 
            'ability_count': ability_count, 
            'ability_data': ability_data}

    def write_skills(self):
        with open('%s%s_skills.csv' % (self.rootdir, self.adventure_name), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Ability',] + self.skill_data['dc_set'])
            for ability in self.skill_data['ability_set']:
                ln = [ability,] + [self.skill_data['ability_data'][ability].count(dc) for dc in self.skill_data['dc_set']]
                writer.writerow(ln)

    def write_saves(self):
        with open('%s%s_saves.csv' % (self.rootdir, self.adventure_name), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Ability',] + self.save_data['dc_set'])
            for ability in self.save_data['ability_set']:
                ln = [ability,] + [self.save_data['ability_data'][ability].count(dc) for dc in self.save_data['dc_set']]
                writer.writerow(ln)

    def write_save_totals(self):
        with open('%s%s_save_totals.csv' % (self.rootdir, self.adventure_name), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Ability', 'Count'] )
            for k, v in self.save_data['ability_data'].items():
                writer.writerow([k, len(v)])

    def write_skill_check_data(self):
        skill_set = set([item['Skill'] for item in self.skill_checks])
        skill_totals = OrderedDict()
        for skill in skill_set:
            skill_totals[skill] = [item['DC'] for item in self.skill_checks if item['Skill'] == skill]
        with open('%s%s_skill_totals.csv' % (self.rootdir, self.adventure_name), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Skill', 'Count', 'Mean'] )
            for skill_label, dc_list in skill_totals.items():
                writer.writerow([skill_label, len(dc_list), numpy.mean(dc_list)])


if __name__ == "__main__":
    rootdir = "dnd_data/rawmodules/"
    for adv in ['wbtw', 'rotf']:
        AdventureParser(rootdir, adv, write_data=False)
    print("Done")