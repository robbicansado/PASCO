#pragma once
// PASCO / FlexDuino V5 — anotacao historica, NAO firmware pronto para gravacao.
// Inferencia estatica a partir do disassembly original em 0x09EA-0x0A00.
// Estes pinos NAO representam o mapeamento experimental atual.
namespace V5Historico {
constexpr unsigned char PINO_SAIDA_CANDIDATO = 11; // pinMode(11, OUTPUT)
constexpr unsigned char PINO_ENTRADA_CANDIDATO = 10; // pinMode(10, INPUT)
constexpr unsigned char PINO_ANALOGICO_CANDIDATO = 14; // pinMode(14, INPUT), A0 no Nano
}
