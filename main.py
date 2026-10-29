from client.main import TeaGuardianApp


if __name__ == '__main__':
    TeaGuardianApp().run()

    def _notify_timer_complete(self):
        if platform == "android":
            try:
                from plyer import vibrator
            except ImportError:
                self.timer_status.text = "Время вышло, вибрация недоступна."
                return
            try:
                if vibrator.exists():
                    vibrator.vibrate(time=1)
                else:
                    self.timer_status.text = "Время вышло, вибрация недоступна."
            except (NotImplementedError, RuntimeError):
                self.timer_status.text = "Время вышло, вибрация недоступна."
            return

        if platform == "win":
            import winsound

            if not winsound.MessageBeep():
                self.timer_status.text = "Время вышло, звуковой сигнал недоступен."
        else:
            print("\a", end="", flush=True)


if __name__ == "__main__":
    TeaGuardianApp().run()
