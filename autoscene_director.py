
# AutoScene Director — Windows foreground window based scene switcher
import obspython as obs
import ctypes, ctypes.wintypes as wt
import re, time

ACTIVE = True
INTERVAL_MS = 500
MAPPINGS = ""  # lines: pattern => Scene Name
last_scene = None
last_title = ""

# win32 APIs
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
GetForegroundWindow = user32.GetForegroundWindow
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextW = user32.GetWindowTextW
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
OpenProcess = kernel32.OpenProcess
QueryFullProcessImageNameW = kernel32.QueryFullProcessImageNameW
CloseHandle = kernel32.CloseHandle
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

def script_description():
    return "Troca a cena com base na janela ativa (Windows)."

def script_properties():
    p = obs.obs_properties_create()
    obs.obs_properties_add_bool(p, "active", "Ativo")
    obs.obs_properties_add_int(p, "interval", "Intervalo (ms)", 100, 5000, 50)
    obs.obs_properties_add_text(p, "mappings", "Mapeamentos (padrao => Cena)", obs.OBS_TEXT_MULTILINE)
    return p

def script_defaults(s):
    obs.obs_data_set_default_bool(s, "active", True)
    obs.obs_data_set_default_int(s, "interval", 500)
    obs.obs_data_set_default_string(s, "mappings", "chrome => Cena Navegador\nobs64.exe => Cena OBS\nVALORANT => Cena Jogo")

def script_update(s):
    global ACTIVE, INTERVAL_MS, MAPPINGS
    ACTIVE = obs.obs_data_get_bool(s, "active")
    INTERVAL_MS = obs.obs_data_get_int(s, "interval")
    MAPPINGS = obs.obs_data_get_string(s, "mappings")
    obs.timer_remove(tick)
    if ACTIVE:
        obs.timer_add(tick, INTERVAL_MS)

def parse_mappings():
    rules = []
    for line in MAPPINGS.splitlines():
        if "=>" not in line: continue
        pat, scene = [x.strip() for x in line.split("=>", 1)]
        if not pat or not scene: continue
        rules.append((pat, scene))
    return rules

def get_foreground_title_exe():
    hwnd = GetForegroundWindow()
    if hwnd == 0:
        return "", ""
    length = GetWindowTextLengthW(hwnd)
    buf = wt.LPWSTR('\0' * (length + 1))
    GetWindowTextW(hwnd, buf, length + 1)
    title = buf.value or ""

    pid = wt.DWORD()
    GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    hproc = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
    exe = ""
    if hproc:
        exe_buf = wt.create_unicode_buffer(260)
        size = wt.DWORD(260)
        if QueryFullProcessImageNameW(hproc, 0, exe_buf, ctypes.byref(size)):
            exe = exe_buf.value.split("\\")[-1]
        CloseHandle(hproc)
    return title, exe

def switch_scene(name):
    global last_scene
    scn = obs.obs_get_source_by_name(name)
    if scn:
        obs.obs_frontend_set_current_scene(scn)
        obs.obs_source_release(scn)
        last_scene = name
        obs.script_log(obs.LOG_INFO, f"Cena trocada para: {name}")
    else:
        obs.script_log(obs.LOG_WARNING, f"Cena não encontrada: {name}")

def tick():
    if not ACTIVE: return
    title, exe = get_foreground_title_exe()
    if not title and not exe: return
    rules = parse_mappings()
    text = (title + " " + exe).lower()
    for pat, scene in rules:
        if pat.lower() in text:
            if scene != last_scene:
                switch_scene(scene)
            break
