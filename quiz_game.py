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