from urllib.parse import quote

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from client.api_client import ApiClient
from client.services.auth_store import AuthStore
from client.theme import APP_BG, CARD_BG, PRIMARY, TEXT_PRIMARY, WHITE


class AuthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = BoxLayout(orientation='vertical', padding=30, spacing=18)
        self.background.canvas.before.clear()
        self.background.canvas.before.add(Color(1, 1, 1, 1))
        self.background.canvas.before.add(Rectangle(pos=self.background.pos, size=self.background.size))

        title = Label(text='TeaGuardian', bold=True, font_size='30sp', color=TEXT_PRIMARY, size_hint_y=None, height=48)
        subtitle = Label(text='Личный чайный дневник', color=(0.46, 0.39, 0.34, 1), size_hint_y=None, height=24)

        self.name_input = TextInput(hint_text='Имя', multiline=False, size_hint_y=None, height=48)
        self.email_input = TextInput(hint_text='Email', multiline=False, size_hint_y=None, height=48)
        self.password_input = TextInput(hint_text='Пароль', multiline=False, password=True, size_hint_y=None, height=48)
        self.status_label = Label(text='', color=(0.7, 0.2, 0.2, 1), size_hint_y=None, height=28)

        actions = BoxLayout(size_hint_y=None, height=52, spacing=12)
        self.submit_btn = Button(text='Войти', background_color=PRIMARY, color=WHITE)
        self.switch_btn = Button(text='Создать аккаунт', background_color=(0.82, 0.65, 0.52, 1), color=WHITE)
        actions.add_widget(self.submit_btn)
        actions.add_widget(self.switch_btn)

        self.submit_btn.bind(on_release=self.handle_submit)
        self.switch_btn.bind(on_release=self.toggle_mode)
        self.show_login_mode()

        self.background.add_widget(title)
        self.background.add_widget(subtitle)
        self.background.add_widget(self.name_input)
        self.background.add_widget(self.email_input)
        self.background.add_widget(self.password_input)
        self.background.add_widget(self.status_label)
        self.background.add_widget(actions)
        self.add_widget(self.background)

    def set_status(self, text, error=False):
        self.status_label.text = text
        self.status_label.color = (0.7, 0.2, 0.2, 1) if error else (0.2, 0.5, 0.3, 1)

    def toggle_mode(self, _instance):
        if self.submit_btn.text == 'Войти':
            self.show_register_mode()
        else:
            self.show_login_mode()

    def show_login_mode(self):
        self.submit_btn.text = 'Войти'
        self.switch_btn.text = 'Создать аккаунт'
        self.name_input.text = ''
        self.name_input.opacity = 0
        self.name_input.disabled = True
        self.name_input.size_hint_y = None
        self.name_input.height = 0

    def show_register_mode(self):
        self.submit_btn.text = 'Регистрация'
        self.switch_btn.text = 'Уже есть аккаунт'
        self.name_input.opacity = 1
        self.name_input.disabled = False
        self.name_input.size_hint_y = None
        self.name_input.height = 48

    def handle_submit(self, _instance):
        app = App.get_running_app()
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if self.submit_btn.text == 'Войти':
            if not email or not password:
                self.set_status('Введите email и пароль', True)
                return
            response, data = app.api.login(email, password)
            if response.ok:
                self.set_status('Успешный вход')
                app.show_recipes()
            else:
                self.set_status(data.get('detail', 'Ошибка входа'), True)
            return

        if not name or not email or not password:
            self.set_status('Заполните имя, email и пароль', True)
            return
        response, data = app.api.register(name, email, password)
        if response.ok:
            self.set_status('Аккаунт создан')
            app.show_recipes()
        else:
            self.set_status(data.get('detail', 'Ошибка регистрации'), True)


class RecipeFormPopup(Popup):
    def __init__(self, app, recipe=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.recipe = recipe
        self.title = 'Добавить рецепт' if recipe is None else 'Редактировать рецепт'
        self.size_hint = (0.9, 0.9)

        container = BoxLayout(orientation='vertical', spacing=12, padding=18)
        container.canvas.before.clear()
        container.canvas.before.add(Color(1, 1, 1, 1))
        container.canvas.before.add(Rectangle(pos=container.pos, size=container.size))

        self.name_input = TextInput(hint_text='Название', multiline=False, text=recipe['name'] if recipe else '')
        self.tea_type_input = TextInput(hint_text='ID типа чая', multiline=False, text=str(recipe['tea_type_id']) if recipe else '1')
        self.temp_input = TextInput(hint_text='Температура °C', multiline=False, text=str(recipe['temperature']) if recipe else '80')
        self.notes_input = TextInput(hint_text='Заметки', multiline=True, text=recipe.get('notes', '') if recipe else '')
        self.private_checkbox = CheckBox(active=recipe.get('is_private', True) if recipe else True)

        row = BoxLayout(size_hint_y=None, height=40)
        row.add_widget(Label(text='Приватный рецепт', color=TEXT_PRIMARY))
        row.add_widget(self.private_checkbox)

        actions = BoxLayout(size_hint_y=None, height=52, spacing=12)
        save_btn = Button(text='Сохранить', background_color=PRIMARY, color=WHITE)
        cancel_btn = Button(text='Отмена', background_color=(0.72, 0.72, 0.72, 1), color=WHITE)
        save_btn.bind(on_release=self.save_recipe)
        cancel_btn.bind(on_release=self.dismiss)
        actions.add_widget(save_btn)
        actions.add_widget(cancel_btn)

        container.add_widget(self.name_input)
        container.add_widget(self.tea_type_input)
        container.add_widget(self.temp_input)
        container.add_widget(self.notes_input)
        container.add_widget(row)
        container.add_widget(actions)
        self.content = container

    def save_recipe(self, _instance):
        try:
            tea_id = int(self.tea_type_input.text)
            temperature = int(self.temp_input.text)
        except ValueError:
            self.app.show_message('Введите корректные числа', error=True)
            return

        payload = {
            'tea_type_id': tea_id,
            'name': self.name_input.text.strip(),
            'temperature': temperature,
            'notes': self.notes_input.text.strip() or None,
            'is_private': self.private_checkbox.active,
        }
        if not payload['name']:
            self.app.show_message('Название рецепта не может быть пустым', error=True)
            return

        if self.recipe is None:
            response, data = self.app.api.post('/recipes', payload)
        else:
            response, data = self.app.api.patch(f"/recipes/{self.recipe['id']}", payload)

        if response.ok:
            self.dismiss()
            self.app.recipe_screen.load_recipes()
        else:
            self.app.show_message(data.get('detail', 'Ошибка сохранения'), error=True)


class TeaTimerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recipe = None
        self.remaining = 0
        self.timer_event = None
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=16)
        self.title = Label(text='Таймер заваривания', bold=True, font_size='24sp', color=TEXT_PRIMARY)
        self.recipe_label = Label(text='', color=TEXT_PRIMARY, font_size='20sp')
        self.time_label = Label(text='00:00', bold=True, font_size='36sp', color=PRIMARY)
        self.status_label = Label(text='Готов к старту', color=(0.2, 0.5, 0.3, 1), size_hint_y=None, height=24)

        buttons = BoxLayout(size_hint_y=None, height=52, spacing=12)
        self.start_btn = Button(text='Старт', background_color=PRIMARY, color=WHITE)
        self.pause_btn = Button(text='Пауза', background_color=(0.82, 0.65, 0.52, 1), color=WHITE)
        self.back_btn = Button(text='Назад', background_color=(0.6, 0.6, 0.6, 1), color=WHITE)
        self.start_btn.bind(on_release=self.start_timer)
        self.pause_btn.bind(on_release=self.pause_timer)
        self.back_btn.bind(on_release=self.back_to_recipes)
        buttons.add_widget(self.start_btn)
        buttons.add_widget(self.pause_btn)
        buttons.add_widget(self.back_btn)

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.recipe_label)
        self.layout.add_widget(self.time_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(buttons)
        self.add_widget(self.layout)

    def set_recipe(self, recipe):
        self.recipe = recipe
        self.remaining = max(60, int(recipe.get('temperature', 80)) * 2)
        self.update_time_label()
        self.recipe_label.text = recipe.get('name', 'Рецепт')
        self.status_label.text = 'Готов к старту'
        if self.timer_event is not None:
            self.timer_event.cancel()
            self.timer_event = None

    def update_time_label(self):
        minutes, seconds = divmod(self.remaining, 60)
        self.time_label.text = f'{minutes:02d}:{seconds:02d}'

    def start_timer(self, _instance):
        if self.timer_event is not None:
            return
        self.status_label.text = 'Заваривание идёт'
        self.timer_event = Clock.schedule_interval(self.tick, 1)

    def pause_timer(self, _instance):
        if self.timer_event is not None:
            self.timer_event.cancel()
            self.timer_event = None
            self.status_label.text = 'Пауза'

    def tick(self, dt):
        if self.remaining <= 0:
            self.pause_timer(None)
            self.status_label.text = 'Чай готов!'
            return
        self.remaining -= 1
        self.update_time_label()
        if self.remaining == 0:
            self.pause_timer(None)
            self.status_label.text = 'Чай готов!'

    def back_to_recipes(self, _instance):
        App.get_running_app().show_recipes()


class RecipeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        self.layout.canvas.before.clear()
        self.layout.canvas.before.add(Color(1, 1, 1, 1))
        self.layout.canvas.before.add(Rectangle(pos=self.layout.pos, size=self.layout.size))

        header = BoxLayout(size_hint_y=None, height=52)
        title = Label(text='Мои рецепты', bold=True, font_size='22sp', color=TEXT_PRIMARY)
        logout = Button(text='Выход', background_color=(0.6, 0.2, 0.2, 1), color=WHITE)
        logout.bind(on_release=self.logout)
        header.add_widget(title)
        header.add_widget(logout)

        search_row = BoxLayout(size_hint_y=None, height=48, spacing=10)
        self.search_input = TextInput(hint_text='Поиск по рецептам', multiline=False)
        search_btn = Button(text='Поиск', background_color=PRIMARY, color=WHITE, size_hint_x=None, width=120)
        search_btn.bind(on_release=self.search_recipes)
        search_row.add_widget(self.search_input)
        search_row.add_widget(search_btn)

        actions = BoxLayout(size_hint_y=None, height=52, spacing=12)
        refresh_btn = Button(text='Обновить', background_color=PRIMARY, color=WHITE)
        add_btn = Button(text='Добавить', background_color=(0.46, 0.75, 0.53, 1), color=WHITE)
        refresh_btn.bind(on_release=self.load_recipes)
        add_btn.bind(on_release=self.open_create_dialog)
        actions.add_widget(refresh_btn)
        actions.add_widget(add_btn)

        self.list_container = BoxLayout(orientation='vertical', spacing=10)
        self.scroll = ScrollView(do_scroll_x=False)
        self.scroll.add_widget(self.list_container)

        self.status = Label(text='', size_hint_y=None, height=24, color=(0.2, 0.5, 0.3, 1))
        self.layout.add_widget(header)
        self.layout.add_widget(search_row)
        self.layout.add_widget(actions)
        self.layout.add_widget(self.status)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def set_status(self, text, error=False):
        self.status.text = text
        self.status.color = (0.7, 0.2, 0.2, 1) if error else (0.2, 0.5, 0.3, 1)

    def logout(self, _instance):
        app = App.get_running_app()
        app.api.logout()
        app.show_auth()

    def open_create_dialog(self, _instance):
        popup = RecipeFormPopup(App.get_running_app())
        popup.open()

    def search_recipes(self, _instance):
        self.load_recipes(search=self.search_input.text.strip())

    def load_recipes(self, _instance=None, search=None):
        app = App.get_running_app()
        query = search if search is not None else self.search_input.text.strip()
        path = '/recipes'
        if query:
            path = f"/recipes?search={quote(query)}"
        response, data = app.api.get(path)
        if response.ok:
            recipes = data if isinstance(data, list) else []
            self.render_recipes(recipes)
            self.set_status(f'Рецептов: {len(recipes)}')
        else:
            self.set_status(data.get('detail', 'Ошибка загрузки'), True)
            if response.status_code in (401, 403):
                app.show_auth()

    def render_recipes(self, recipes):
        self.list_container.clear_widgets()
        if not recipes:
            empty = Label(text='Пока нет рецептов', color=TEXT_PRIMARY)
            self.list_container.add_widget(empty)
            return

        for recipe in recipes:
            item = BoxLayout(size_hint_y=None, height=120, spacing=10, padding=(10, 8))
            item.canvas.before.clear()
            item.canvas.before.add(Color(0.96, 0.93, 0.89, 1))
            item.canvas.before.add(Rectangle(pos=item.pos, size=item.size))

            label = Label(
                text=f"{recipe['name']}\n{recipe['temperature']}°C",
                color=TEXT_PRIMARY,
                halign='left',
                valign='middle',
                text_size=(self.width - 240, None),
                size_hint_x=1,
            )
            actions = BoxLayout(size_hint_x=None, width=240, spacing=8)
            timer_btn = Button(text='Таймер', background_color=(0.46, 0.7, 0.86, 1), color=WHITE, size_hint_x=0.6)
            edit_btn = Button(text='Изм.', background_color=PRIMARY, color=WHITE, size_hint_x=0.5)
            delete_btn = Button(text='Удал.', background_color=(0.7, 0.2, 0.2, 1), color=WHITE, size_hint_x=0.5)
            timer_btn.bind(on_release=lambda _btn, r=recipe: self.open_timer(r))
            edit_btn.bind(on_release=lambda _btn, r=recipe: self.edit_recipe(r))
            delete_btn.bind(on_release=lambda _btn, r=recipe: self.delete_recipe(r))
            actions.add_widget(timer_btn)
            actions.add_widget(edit_btn)
            actions.add_widget(delete_btn)
            item.add_widget(label)
            item.add_widget(actions)
            self.list_container.add_widget(item)

    def open_timer(self, recipe):
        app = App.get_running_app()
        app.timer_screen.set_recipe(recipe)
        app.show_timer()

    def edit_recipe(self, recipe):
        popup = RecipeFormPopup(App.get_running_app(), recipe=recipe)
        popup.open()

    def delete_recipe(self, recipe):
        app = App.get_running_app()
        response, data = app.api.delete(f"/recipes/{recipe['id']}")
        if response.ok:
            self.load_recipes()
        else:
            self.set_status(data.get('detail', 'Ошибка удаления'), True)


class TeaGuardianApp(App):
    title = 'TeaGuardian'
    app_bg = APP_BG
    card_bg = CARD_BG
    primary = PRIMARY
    theme_text = TEXT_PRIMARY
    button_text = WHITE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_store = AuthStore(self.user_data_dir)
        self.api = ApiClient(self.auth_store)
        self.sm = ScreenManager()
        self.auth_screen = AuthScreen(name='auth')
        self.recipe_screen = RecipeScreen(name='recipes')
        self.timer_screen = TeaTimerScreen(name='timer')
        self.sm.add_widget(self.auth_screen)
        self.sm.add_widget(self.recipe_screen)
        self.sm.add_widget(self.timer_screen)

    def build(self):
        self.show_auth()
        return self.sm

    def show_auth(self):
        self.sm.current = 'auth'

    def show_recipes(self):
        self.recipe_screen.load_recipes()
        self.sm.current = 'recipes'

    def show_timer(self):
        self.sm.current = 'timer'

    def show_message(self, text, error=False):
        if self.sm.current == 'recipes':
            self.recipe_screen.set_status(text, error)
        else:
            self.auth_screen.set_status(text, error)


if __name__ == '__main__':
    TeaGuardianApp().run()
