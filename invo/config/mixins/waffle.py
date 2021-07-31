from configurations import values

from ..values import LogLevelValue


class Waffle:
    WAFFLE_COOKIE = values.Value("dwf_%s")
    WAFFLE_TEST_COOKIE = values.Value("dwft_%s")
    WAFFLE_SECURE = values.BooleanValue(True)
    WAFFLE_MAX_AGE = values.IntegerValue(2592000)  # 1 month in seconds

    WAFFLE_CACHE_PREFIX = values.Value("waffle:")
    WAFFLE_CACHE_NAME = values.Value("default")
    WAFFLE_FLAG_CACHE_KEY = values.Value("flag:%s")
    WAFFLE_FLAG_USERS_CACHE_KEY = values.Value("flag:%s:users")
    WAFFLE_FLAG_GROUPS_CACHE_KEY = values.Value("flag:%s:groups")
    WAFFLE_ALL_FLAGS_CACHE_KEY = values.Value("flags:all")
    WAFFLE_SAMPLE_CACHE_KEY = values.Value("sample:%s")
    WAFFLE_ALL_SAMPLES_CACHE_KEY = values.Value("samples:all")
    WAFFLE_SWITCH_CACHE_KEY = values.Value("switch:%s")
    WAFFLE_ALL_SWITCHES_CACHE_KEY = values.Value("switches:all")

    WAFFLE_FLAG_DEFAULT = values.BooleanValue(False)
    WAFFLE_SWITCH_DEFAULT = values.BooleanValue(False)
    WAFFLE_SAMPLE_DEFAULT = values.BooleanValue(False)

    WAFFLE_CREATE_MISSING_FLAGS = values.BooleanValue(False)
    WAFFLE_CREATE_MISSING_SAMPLES = values.BooleanValue(False)
    WAFFLE_CREATE_MISSING_SWITCHES = values.BooleanValue(False)

    WAFFLE_READ_FROM_WRITE_DB = values.BooleanValue(False)

    # FIX: These don't seem to be reading from the env
    WAFFLE_LOG_MISSING_FLAGS = LogLevelValue(None)
    WAFFLE_LOG_MISSING_SAMPLES = LogLevelValue(None)
    WAFFLE_LOG_MISSING_SWITCHES = LogLevelValue(None)

    WAFFLE_CACHE_NAME = values.Value("default")
