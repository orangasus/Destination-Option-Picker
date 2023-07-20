import csv
import googlemaps
from SummaryRoute import SummaryRoute


with open('maps_key.txt', 'r') as file:
    MAPS_API_KEY = file.readline()
map_client = googlemaps.Client(key=MAPS_API_KEY)

csv_summary_writer = None
summary_db = open('summary_db.csv', 'w', newline='')

origins = []
options = []
travel_mode = None

summary_list = {}


def read_input_and_setup():
    global origins, options, travel_mode
    with open('input.txt', 'r') as file:
        origins = list(set([x for x in file.readline().rstrip('\n').split(';')]))
        options = list(set([x for x in file.readline().rstrip('\n').split(';')]))
        travel_mode = file.readline()
    options = [el + ", Oulu" for el in options]
    for el in origins:
        summary_list[el] = []


def set_up_csv_file():
    global csv_summary_writer
    field_names_summary = ['Origin', 'Destination', 'Avg Time, min', 'Avg Distance, km', 'Num of Routes']
    csv_summary_writer = csv.DictWriter(f=summary_db, fieldnames=field_names_summary, delimiter=';')
    csv_summary_writer.writeheader()


def list_all_routes(start, finish, travel_mode):
    req = map_client.directions(origin=start, destination=finish, mode=travel_mode, alternatives=True)
    avg_dis, avg_dur = 0, 0
    num_routes = 0
    for route in req:
        distance, duration = route["legs"][0]["distance"]["value"], route["legs"][0]["duration"]["value"]
        avg_dur += duration
        avg_dis += distance
        num_routes += 1

    avg_dis = round(avg_dis / num_routes / 1000, 1)
    avg_dur = round(avg_dur / num_routes / 60)
    summary_list[start].append(SummaryRoute(start, finish, avg_dur, avg_dis, num_routes))


def sort_routes_list():
    global summary_list
    for key in summary_list.keys():
        summary_list[key] = sorted(summary_list[key])


def lists_to_csv():
    global csv_summary_writer
    set_up_csv_file()
    for key in summary_list.keys():
        for el in summary_list[key]:
            csv_summary_writer.writerow(
                {'Origin': el.origin, 'Destination': el.destination, 'Avg Time, min': el.avg_time,
                 'Avg Distance, km': el.avg_dis,
                 'Num of Routes': el.num_routes})
    summary_db.close()

def find_best_option_for_each_origin():
    ans = []
    for key in summary_list.keys():
        ans.append(min(summary_list[key]))
    return ans


if __name__ == '__main__':
    read_input_and_setup()

    for st_loc in origins:
        for end_loc in options:
            try:
                list_all_routes(st_loc, end_loc, travel_mode)
            except Exception as e:
                print(e, st_loc, end_loc)

    sort_routes_list()
    lists_to_csv()

    best_options = find_best_option_for_each_origin()
    for el in best_options:
        print(el,end='\n\n')
