
import json
import random
import os

city = {
    "name": "MY CITY",
    "money": 300_000_000,
    "population": 500,
    "happiness": 75,
    "day": 1,
    "tax": 10,
    "bank": 0,
    "debt": 0,
    "buildings": {
        "house": 2,
        "shop": 1,
        "factory": 0,
        "power": 1,
        "water": 1,
        "park": 1
    }
}

BUILDINGS = {
    "house": ("주택", 5_000_000),
    "shop": ("상가", 8_000_000),
    "factory": ("공장", 15_000_000),
    "power": ("발전소", 20_000_000),
    "water": ("수도시설", 12_000_000),
    "park": ("공원", 5_000_000)
}


def capacity():
    return city["buildings"]["house"] * 500


def power():
    return city["buildings"]["power"] * 1000


def water():
    return city["buildings"]["water"] * 1000


def status():
    b = city["buildings"]

    print("\n" + "=" * 45)
    print("             CITY TYCOON")
    print("=" * 45)
    print("도시:", city["name"])
    print("날짜:", city["day"], "일차")
    print(f"자금: {city['money']:,}원")
    print(f"인구: {city['population']:,}명")
    print(f"주택 수용력: {capacity():,}명")
    print(f"행복도: {city['happiness']}%")
    print(f"세율: {city['tax']}%")
    print(f"은행 예금: {city['bank']:,}원")
    print(f"대출: {city['debt']:,}원")
    print("-" * 45)

    for key, (name, cost) in BUILDINGS.items():
        print(f"{name}: {b[key]}개")

    print("-" * 45)
    print(f"전력 공급: {power():,}")
    print(f"수도 공급: {water():,}")
    print("=" * 45)


def build():
    keys = list(BUILDINGS)

    print("\n========== 건설 ==========")

    for i, key in enumerate(keys, 1):
        name, cost = BUILDINGS[key]
        print(f"{i}. {name} - {cost:,}원")

    print("0. 취소")

    try:
        choice = int(input("건설 선택: "))
    except ValueError:
        print("숫자를 입력하세요.")
        return

    if choice == 0:
        return

    if not 1 <= choice <= len(keys):
        print("잘못된 번호입니다.")
        return

    key = keys[choice - 1]
    name, cost = BUILDINGS[key]

    if city["money"] < cost:
        print("자금이 부족합니다.")
        return

    city["money"] -= cost
    city["buildings"][key] += 1

    print(name, "건설 완료!")


def change_tax():
    try:
        rate = int(input("세율 입력 (0~30): "))
    except ValueError:
        print("숫자를 입력하세요.")
        return

    if 0 <= rate <= 30:
        city["tax"] = rate
        print("세율 변경 완료!")
    else:
        print("세율은 0~30 사이여야 합니다.")


def bank():
    print("\n1. 예금")
    print("2. 출금")
    print("3. 대출")
    print("4. 대출 상환")
    print("0. 돌아가기")

    choice = input("선택: ")

    try:
        if choice == "1":
            amount = int(input("예금액: "))
            if 0 < amount <= city["money"]:
                city["money"] -= amount
                city["bank"] += amount
                print("예금 완료")

        elif choice == "2":
            amount = int(input("출금액: "))
            if 0 < amount <= city["bank"]:
                city["bank"] -= amount
                city["money"] += amount
                print("출금 완료")

        elif choice == "3":
            amount = int(input("대출액: "))
            if 0 < amount <= 100_000_000:
                city["money"] += amount
                city["debt"] += amount
                print("대출 완료")

        elif choice == "4":
            amount = int(input("상환액: "))
            if 0 < amount <= min(city["money"], city["debt"]):
                city["money"] -= amount
                city["debt"] -= amount
                print("상환 완료")

    except ValueError:
        print("숫자를 입력하세요.")


def random_event():
    event = random.randint(1, 10)

    if event == 1:
        city["money"] += 10_000_000
        print("기업 투자 유치! 1,000만원 획득")

    elif event == 2:
        damage = min(city["money"], 5_000_000)
        city["money"] -= damage
        print(f"재난 발생! {damage:,}원 피해")

    elif event == 3:
        city["happiness"] = min(
            100, city["happiness"] + 10
        )
        print("도시 축제! 행복도 상승")

    elif event == 4:
        new_people = random.randint(20, 100)
        city["population"] += new_people
        print(f"인구 {new_people}명 유입!")

    else:
        print("특별한 이벤트 없음")


def next_day():
    b = city["buildings"]
    population = city["population"]

    tax_income = int(
        population * 1000 * city["tax"] / 100
    )

    business_income = (
        b["shop"] * 300_000
        + b["factory"] * 700_000
    )

    expenses = (
        b["house"] * 50_000
        + b["shop"] * 100_000
        + b["factory"] * 200_000
        + b["power"] * 300_000
        + b["water"] * 150_000
        + b["park"] * 50_000
    )

    interest = int(city["debt"] * 0.001)
    bank_interest = int(city["bank"] * 0.0005)

    income = tax_income + business_income
    net = income - expenses - interest

    city["money"] += net
    city["bank"] += bank_interest

    city["day"] += 1

    print("\n========== 하루 정산 ==========")
    print(f"세금 수입: {tax_income:,}원")
    print(f"사업 수입: {business_income:,}원")
    print(f"유지비: {expenses:,}원")
    print(f"대출 이자: {interest:,}원")
    print(f"은행 이자: {bank_interest:,}원")
    print(f"오늘 순손익: {net:,}원")

    if population > power() or population > water():
        city["happiness"] -= 8
        print("전력 또는 수도 부족!")
    else:
        city["happiness"] += 2

    if city["tax"] >= 20:
        city["happiness"] -= 3

    city["happiness"] += min(b["park"], 2)

    city["happiness"] = max(
        0, min(100, city["happiness"])
    )

    room = max(0, capacity() - population)

    if (
        room > 0
        and population <= power()
        and population <= water()
        and city["happiness"] >= 30
    ):
        growth = min(room, random.randint(20, 60))
        city["population"] += growth
        print(f"인구 {growth}명 증가!")

    elif city["happiness"] < 20:
        loss = min(population, random.randint(5, 20))
        city["population"] -= loss
        print(f"인구 {loss}명 감소!")

    random_event()

    print("하루가 종료되었습니다.")


def save():
    with open("city_save.json", "w", encoding="utf-8") as f:
        json.dump(city, f, ensure_ascii=False, indent=4)
    print("저장 완료!")


def load():
    global city

    if not os.path.exists("city_save.json"):
        print("저장 파일이 없습니다.")
        return

    try:
        with open("city_save.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        required = {
            "name", "money", "population", "happiness",
            "day", "tax", "bank", "debt", "buildings"
        }

        if not required.issubset(data):
            raise ValueError("필수 데이터 누락")

        if not set(BUILDINGS).issubset(data["buildings"]):
            raise ValueError("건물 데이터 누락")

        city = data
        print("불러오기 완료!")

    except (ValueError, TypeError, KeyError, OSError):
        print("저장 파일이 손상되었거나 형식이 잘못되었습니다.")


def main():
    print("CITY TYCOON TEXT EDITION")

    while True:
        print("\n========== 메인 메뉴 ==========")
        print("1. 도시 현황")
        print("2. 건물 건설")
        print("3. 하루 진행")
        print("4. 세율 변경")
        print("5. 은행")
        print("6. 저장")
        print("7. 불러오기")
        print("0. 종료")

        choice = input("선택: ")

        if choice == "1":
            status()
        elif choice == "2":
            build()
        elif choice == "3":
            next_day()
        elif choice == "4":
            change_tax()
        elif choice == "5":
            bank()
        elif choice == "6":
            save()
        elif choice == "7":
            load()
        elif choice == "0":
            print("게임 종료!")
            break
        else:
            print("잘못된 선택입니다.")


if __name__ == "__main__":
    main()
