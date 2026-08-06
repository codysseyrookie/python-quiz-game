import json
from pathlib import Path

class QuizGame:
    def __init__(self):
        # 파일 경로 설정
        self.quiz_file = Path(__file__).with_name("quiz_data.json")
        self.state_file = Path(__name__).with_name("state.json")

        self.quizzes = []
        self.best_score = 0
        
        # 데이터 로드
        self.load_quizzes()
        self.load_state()

    def load_quizzes(self):
        """quiz_data.json에서 'quizzes' 키의 리스트를 불러옵니다."""
        if not self.quiz_file.exists():
            self.quizzes = []
            return
        try:
            with self.quiz_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = data.get("quizzes", [])
        except (json.JSONDecodeError, OSError):
            self.quizzes = []

    def load_state(self):
        """state.json에서 최고 점수를 불러옵니다."""
        if not self.state_file.exists():
            self.best_score = 0
            return
        try:
            with self.state_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_score = data.get("best_score", 0)
        except (json.JSONDecodeError, OSError):
            self.best_score = 0

    def save_state(self):
        """최고 점수를 state.json에 저장합니다."""
        try:
            with self.state_file.open("w", encoding="utf-8") as f:
                json.dump({"best_score": self.best_score}, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"상태 저장 실패: {e}")

    def show_menu(self):
        """메뉴를 화면에 출력합니다."""
        print("\n" + "="*20)
        print("   파이썬 퀴즈 게임")
        print("="*20)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가하기")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 종료하기")
        print("="*20)

    def play_quiz(self):
        """퀴즈 게임을 진행합니다."""
        if not self.quizzes:
            print("\n문제가 없습니다. 퀴즈를 먼저 추가해주세요!")
            return

        score = 0
        print("\n--- 게임 시작! ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"\nQ{i}. {q['question']}")
            for idx, choice in enumerate(q['choices'], 1):
                print(f"  {idx}) {choice}")
            
            try:
                user_ans = int(input("정답 번호 입력: "))
                if user_ans == q['answer']:
                    print("정답입니다! ✨")
                    score += 20 # 한 문제당 20점 (5문제 기준 100점)
                else:
                    print(f"틀렸습니다. 정답은 {q['answer']}번입니다. 😢")
            except ValueError:
                print("숫자만 입력 가능합니다. 이번 문제는 틀린 것으로 처리됩니다.")

        print(f"\n게임 종료! 당신의 점수는 {score}점입니다.")
        
        if score > self.best_score:
            print(f"🎊 축하합니다! 최고 점수 경신! ({self.best_score} -> {score})")
            self.best_score = score
            self.save_state()

    def add_quiz(self):
        """새로운 퀴즈를 추가합니다."""
        print("\n--- 새 퀴즈 추가 ---")
        question = input("질문: ")
        choices = []
        for i in range(1, 5):
            choices.append(input(f"선택지 {i}: "))
        
        try:
            answer = int(input("정답 번호 (1~4): "))
            new_quiz = {
                "question": question,
                "choices": choices,
                "answer": answer
            }
            self.quizzes.append(new_quiz)
            # JSON 저장 로직 (quizzes 키 구조 유지)
            with self.quiz_file.open("w", encoding="utf-8") as f:
                json.dump({"quizzes": self.quizzes}, f, ensure_ascii=False, indent=2)
            print("성공적으로 저장되었습니다!")
        except ValueError:
            print("잘못된 입력입니다. 추가가 취소되었습니다.")

    def show_quiz_list(self):
        """등록된 퀴즈 목록을 보여줍니다."""
        print("\n--- 퀴즈 목록 ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q['question']}")

    def run(self):
        try:
            """메인 루프"""
            while True:
                self.show_menu()
                choice = input("선택: ").strip()
                if choice == "1": self.play_quiz()
                elif choice == "2": self.add_quiz()
                elif choice == "3": self.show_quiz_list()
                elif choice == "4": print(f"\n최고 점수: {self.best_score}점")
                elif choice == "5": 
                    print("게임을 종료합니다.")
                    break
                else: print("잘못된 입력입니다.")
        except KeyboardInterrupt:
            # Ctrl+C를 눌렀을 때 실행될 코드
            print("\n\n사용자에 의해 프로그램이 강제 종료되었습니다. 안녕히 가세요!")