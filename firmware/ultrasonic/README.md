# Ultrasonic firmware recovery

These two sketches are preserved from the local PASCO archive and serve different purposes.

| Sketch | Pin mapping | Behavior |
|---|---|---|
| [ultrassom_ref.ino](ultrassom_ref/ultrassom_ref.ino) | TRIG 8 / ECHO 9 | Generates an ultrasonic trigger and calls `pulseIn`, but **does not calculate or print distance**. |
| [sketch_aug19b.ino](sketch_aug19b/sketch_aug19b.ino) | TRIG 7 / ECHO 6 | Diagnostic for an HC-SR04 directly attached to a Nano; prints echo duration and computed distance in cm at 9600 baud. |

The two sketches use **different wiring** and should not be treated as interchangeable without checking the actual connections. The speed-of-sound conversion in the second sketch is approximate. These are archived diagnostic versions, not evidence of complete ultrasonic system validation.

See [Technical Report 09](../../docs/relatorios/Relatorio_09_Validacao_Comparativa_do_Sistema_Ultrassonico.pdf) for the experimental comparison.
