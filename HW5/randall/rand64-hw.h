_Bool
rdrand_supported (void);

void
hardware_rand64_init (char *file);

unsigned long long
hardware_rand64 (void);

void
hardware_rand64_fini (void);
