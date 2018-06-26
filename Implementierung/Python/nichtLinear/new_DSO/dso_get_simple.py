# Bibliothek einbinden:
import lib.rftools_remote_lecroy_waverunner as rftools_remote_wr

# USB-ID des Oszilloskops (stehet unter Reiter „Remote“ in der Scope-Software):
scope_id = 'USB0::0x05FF::0x1023::3808N60406::INSTR'

# Verbindung zum Scope herstellen:
scope = rftools_remote_wr.LeCroyWaveRunner(scope_id)
if not scope.valid_connection:
    print('Verbindung fehlgeschlagen')

# Scope-Einstellungen verändern (optional):
# scope.set_realtime_mode()
# scope.set_horizontal_range(time_per_division=1e-6)
# scope.set_vertical_range(volt_per_division=1.0, channel_number=1)
# scope.set_maximum_number_of_samples(max_number_of_samples=1000)

# Triggern (optional):
# print('Starte Trigger')
# scope.trigger_single(trigger_channel=1, trigger_level=0.0)
# if not scope.flag_valid_trigger:
#     print('Trigger fehlgeschlagen')

# Daten auslesen (z.B. Kanal 1):
scope.read(channel_number=1)
t = scope.t
y = scope.y

# Alternativ:
#t, y = scope.return_data(segment_number=1)
