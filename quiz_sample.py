import json
from numpy import random as rnd

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def input_int(message, max, min):
    while True: # ずっとループ
        ip_data = input(message) # キーボード入力させる

        try:
            int_data = int(ip_data) # 入力値をint型に変換

            if int_data in range(min,max+1): # intに変換した入力値がminとmaxの範囲内にある場合
                return int_data # intに変換した入力値を返す(ここでループを抜ける)

            else: # 範囲外の場合
                print("数値の範囲が不正です。")

        except: # 上でエラーになる場合(intに変換できない場合)
            print("数値で入力してください。")

def quiz(num=10):
    """
        引数 num
            デフォルト値10 この関数を呼ぶときに引数を指定しないと、この値が適用される
    """

    json_file = "quiz.json"
    quiz_list = read_json(json_file) # クイズの問題をlistで受け取ります
    rnd.shuffle(quiz_list) # クイズの問題をシャッフルします

    if len(quiz_list) < num: # 引数numがクイズの問題の総数を超える場合
        num = len(quiz_list) # numをクイズの総数とする

    correct = 0 # 正解数初期化
    for _ in range(num): # num回 forループを回す
        quiz_data = quiz_list.pop() # クイズの問題をひとつ取り出します

        # quiz_dataから難易度を取り出します
        # jsonに設定されている難易度が負なら0、6以上なら5としたい
        difficulty = min(max(quiz_data["Difficulty"], 0), 5)

        # 難易度表示の文字列を作成
        stars = f"(難易度{'★' * difficulty}{'☆' * (5 - difficulty)})"

        question = quiz_data["Qestion"] # quiz_dataから問題文を取り出します
        choices = quiz_data["Choices"] # quiz_dataから選択肢を取り出します
        answer = choices[quiz_data["Answer"]] # quiz_dataから正解の要素番号を取り出し、選択肢から正解を取り出します
        rnd.shuffle(choices) # 選択肢をシャッフルします

        print(question) # 問題文を表示
        print(stars) # 難易度を表示
        for i in range(len(choices)):
            print(i+1, choices[i]) # 選択肢と番号を表示 番号は1から表示したいのでi+1としている

        # 選択した番号を入力させる 選択肢の番号は1から表示しているが、listの要素番号は0からなので入力値から1引いている
        selection = input_int(":", len(choices), 1) - 1 

        if choices[selection] == answer: # 選択した選択肢の要素が正解と等しければ
            print("正解\n") # 正解と表示
            correct += 1 # 正解数に1を加算する
        else: # 等しくなければ
            print("不正解\n") # 不正解と表示

    # 正解数と正答率を表示
    # print(num +" 問中 " + correct + " 問正解しました。(正答率:" + str(int(correct/num*100)) + "%)")
    print(f"{num} 問中 {correct} 問正解しました。(正答率:{int(correct/num*100)}%)")

quiz(10)