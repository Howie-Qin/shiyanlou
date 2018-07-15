def analysis(file, user_id):
    import pandas as pd
    try:
        df = pd.read_json(file)
    except ValueError:
        return 0,0

    data = df[df.user_id==user_id].minutes
    return data.count(), data.sum()


def analysis_raw(file, user_id):
    import json
    times, minutes = 0, 0
    with open(file) as f:
        data = json.load(f)
    for i in data:
        if i['user_id'] == user_id:
            times += 1
            minutes += i['minutes']
    return times, minutes

if __name__ == "__main__":
   # print(analysis('user_study.json', 199071))
    print(analysis_raw('user_study.json', 199071))
