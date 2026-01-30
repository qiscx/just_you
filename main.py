from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from datetime import datetime, timedelta

class just_you(MDApp):
    def build(self):
        self.store = JsonStore('lock_data.json')
        if not self.store.exists('settings'):
            self.store.put('settings', last_unlock=datetime.min.isoformat())
        
        self.time_remaining = 7200
        self.locked = False
        
        self.screen = MDScreen()
        
        self.timer_label = MDLabel(
            text="02:00:00",
            halign="center",
            font_style="H2",
            theme_text_color="Primary"
        )
        
        self.unlock_btn = MDRaisedButton(
            text="ONE-TIME UNLOCK",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            on_release=self.use_weekly_token,
            opacity=0,
            disabled=True
        )
        
        self.screen.add_widget(self.timer_label)
        self.screen.add_widget(self.unlock_btn)
        
        Clock.schedule_interval(self.check_system_theme, 1)
        Clock.schedule_interval(self.tick, 1)
        
        return self.screen

    def check_system_theme(self, dt):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Configuration = autoclass('android.content.res.Configuration')
            res = PythonActivity.mActivity.getResources().getConfiguration()
            is_dark = (res.uiMode & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES
            self.theme_cls.theme_style = "Dark" if is_dark else "Light"
        except:
            hr = datetime.now().hour
            self.theme_cls.theme_style = "Dark" if (hr < 7 or hr > 19) else "Light"

    def tick(self, dt):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            m, s = divmod(self.time_remaining, 60)
            h, m = divmod(m, 60)
            self.timer_label.text = f"{h:02d}:{m:02d}:{s:02d}"
        else:
            self.trigger_lock()

    def trigger_lock(self):
        if not self.locked:
            self.locked = True
            self.unlock_btn.opacity = 1
            self.unlock_btn.disabled = False
        
        self.timer_label.text = "TIME EXPIRED"
        
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            activity = PythonActivity.mActivity
            intent = Intent(activity, activity.getClass())
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
            activity.startActivity(intent)
        except:
            pass

    def use_weekly_token(self, instance):
        data = self.store.get('settings')
        last_use = datetime.fromisoformat(data['last_unlock'])
        
        if datetime.now() >= last_use + timedelta(days=7):
            self.time_remaining = 7200
            self.locked = False
            self.unlock_btn.opacity = 0
            self.unlock_btn.disabled = True
            self.store.put('settings', last_unlock=datetime.now().isoformat())
        else:
            diff = (last_use + timedelta(days=7)) - datetime.now()
            self.timer_label.text = f"LOCKED: {diff.days}d {diff.seconds//3600}h left"

if __name__ == "__main__":
    just_you().run()