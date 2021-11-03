from tika import parser
from phrases import *

class snapshot_organizer:
    def __init__(self):
        #List Creation
        self.raw_list = parser.from_file("leaked-snapshot.pdf")["content"].splitlines()
        for line in self.raw_list:
            for phrase in remove_list:
                if line.find(phrase) >= 0:
                    self.raw_list[self.raw_list.index(line)] = ""
                    break
            if line == "Individuals":
                self.refined_list = list(filter(None, self.raw_list[0:self.raw_list.index(line)]))
                break

        #Dictionary List Creation
        def name_category_region(self, dict, line, category, known_region=""):
            dict["name"] = str(line[0:(line.find(category)-1)])
            temp_string = line.replace(dict["name"], "")
            dict["category"] = category
            temp_string = temp_string.replace(" " + category, "")
            if len(known_region) > 0:
                dict["region"] = known_region
                temp_string = temp_string.replace(" " + known_region, "")
            else:
                for region in region_list:
                    if temp_string.find(region) >= 0:
                        dict["region"].append(region)
                        temp_string = temp_string.replace(" " + region, "")
            return temp_string

        def clean_append(self, dict, key, value, temp_string, append=False):
            dict[key] = value
            temp_string = temp_string.replace(" " + dict[key], "")
            if append == True: self.dict_list.append(dict)

        self.dict_list = []
        for line in self.refined_list:
            dict = {
                "name" : "",
                "category" : "",
                "region" : [],
                "description" : "",
                "affiliation" : "",
                "SDGT" : False
            }
            if line.find("Terror") > 0:
                temp_string = name_category_region(self, dict, line, "Terror")
                if temp_string.find("SDGT") > 0:
                    dict["SDGT"] == True
                    temp_string = temp_string.rstrip(" SDGT")
                if temp_string.find("Media Wing") > 0:
                    clean_append(self, dict, "description", "Media Wing", temp_string)
                clean_append(self, dict, "affiliation", temp_string.lstrip(","), temp_string, True)
            elif line.find("Crime") > 0:
                name_category_region(self, dict, line, "Crime")
                self.dict_list.append(dict)
            elif line.find("Hate") > 0:
                temp_string = name_category_region(self, dict, line, "Hate")
                clean_append(self, dict, "description", temp_string.lstrip(), temp_string, True)
            elif line.find("Militarized Social Movement") > 0:
                temp_string = name_category_region(self, dict, line, "Militarized Social Movement", "United States")
                clean_append(self, dict, "description", temp_string.lstrip(), temp_string, True)
            else:
                name_category_region(self, dict, line, "Violent Non-State Actor")
                self.dict_list.append(dict)

    #Trouble-shooting functions
    def print_list(self, refined_selector):
        if refined_selector == True:
            print(self.refined_list)
        elif refined_selector == False:
            print(self.raw_list)

    def print_list_len(self, refined_selector):
        if refined_selector == True:
            print("Refined List Count: " + str(len(self.refined_list)))
        elif refined_selector == False:
            print("Raw List Count: " + str(len(self.raw_list)))

    def print_dict(self):
        for dict in self.dict_list:
            (print(str(dict) + "\n"))

if __name__ == '__main__':
    snapshot_obj = snapshot_organizer()
    snapshot_obj.print_dict()
