import json
from pathlib import Path


class QuizGame:
    """4지선다형 퀴즈를 등록하고 풀 수 있는 콘솔 프로그램."""

    def __init__(self, data_file=None):
        if data_file is None:
            data_file = Path(__file__).with_name("quiz_data.json")

        self.data_file = Path(data_file)
        self.quizzes = []
        self.best_score = 0
        self.load_state()

    def load_state(self):
        """저장된 퀴즈와 최고 점수를 불러온다."""
        if not self.data_file.exists():
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.quizzes = data.get("quizzes", [])
            self.best_score = data.get("best_score", 0)
        except (OSError, json.JSONDecodeError, TypeError):
            print("저장 파일을 읽지 못해 새 게임으로 시작합니다.")
            self.quizzes = []
            self.best_score = 0

    def save_state(self):
        """퀴즈와 최고 점수를 JSON 파일에 저장한다."""
        data = {
            "quizzes": self.quizzes,
            "best_score": self.best_score,
        }

        try:
            with self.data_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"저장 중 오류가 발생했습니다: {error}")

    def show_menu(self):
        print("\n=== 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 등록")
        print("3. 등록된 퀴즈 보기")
        print("4. 최고 점수 보기")
        print("5. 종료")

    def play_quiz(self):
        """등록된 퀴즈를 순서대로 출제하고 결과를 채점한다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 등록하세요.")
            return

        correct_count = 0

        for question_number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{question_number}번 문제] {quiz['question']}")

            # 각 퀴즈의 보기 4개를 순서대로 출력한다.
            for option_number, option in enumerate(quiz["options"], start=1):
                print(f"{option_number}. {option}")

            # 숫자가 아니거나 1~4 범위를 벗어나면 다시 입력받는다.
            while True:
                answer = input("정답 번호(1~4): ").strip()
                if answer in {"1", "2", "3", "4"}:
                    answer_number = int(answer)
                    break
                print("1~4 사이의 숫자를 입력하세요.")

            if answer_number == quiz["answer"]:
                correct_count += 1
                print("정답입니다!")
            else:
                correct_option = quiz["options"][quiz["answer"] - 1]
                print(
                    f"오답입니다. 정답은 {quiz['answer']}번 "
                    f"'{correct_option}'입니다."
                )

        total_count = len(self.quizzes)
        score = round(correct_count / total_count * 100)

        print("\n=== 최종 결과 ===")
        print(f"맞힌 문제 수: {correct_count}/{total_count}")
        print(f"최종 점수: {score}점")

        if score > self.best_score:
            self.best_score = score
            print(f"최고 점수가 {self.best_score}점으로 갱신되었습니다!")
        else:
            print(f"현재 최고 점수: {self.best_score}점")

    def input_number(self, message, minimum, maximum):
        while True:
            value = input(message).strip()

            if not value.isdigit():
                print("숫자를 입력하세요.")
                continue

            number = int(value)

            if minimum <= number <= maximum:
                return number

            print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")

    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")

        while True:
            question = input("문제를 입력하세요: ").strip()

            if question:
                break

            print("문제를 입력해야 합니다.")

        options = []

        for option_number in range(1, 5):
            while True:
                option = input(f"선택지 {option_number}: ").strip()

                if option:
                    options.append(option)
                    break

                print("선택지를 입력해야 합니다.")

        answer = self.input_number("정답 번호(1~4): ", 1, 4)

        quiz = {
            "question": question,
            "options": options,
            "answer": answer,
        }

        self.quizzes.append(quiz)

        print("퀴즈가 추가되었습니다.")


    def show_quiz_list(self):
        """등록된 퀴즈의 문제를 번호와 함께 출력한다."""
        total_count = len(self.quizzes)

        print(f"\n등록된 퀴즈 목록: 총 {total_count}개")

        if total_count == 0:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print()

        for question_number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{question_number}] {quiz['question']}")

    def show_best_score(self):
        print(f"현재 최고 점수는 {self.best_score}점입니다.")

    def run(self):
        while True:
            self.show_menu()
            choice = input("선택: ").strip()

            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.add_quiz()
            elif choice == "3":
                self.show_quiz_list()
            elif choice == "4":
                self.show_best_score()
            elif choice == "5":
                self.save_state()
                print("프로그램을 종료합니다.")
                break
            else:
                print("1~5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    QuizGame().run()
