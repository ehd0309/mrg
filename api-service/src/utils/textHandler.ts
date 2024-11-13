const initialConsonants = [
  "G",
  "KK",
  "N",
  "D",
  "TT",
  "R",
  "M",
  "B",
  "PP",
  "S",
  "SS",
  "",
  "J",
  "JJ",
  "CH",
  "K",
  "T",
  "P",
  "H",
];
const medialVowels = [
  "A",
  "AE",
  "YA",
  "YAE",
  "EO",
  "E",
  "YEO",
  "YE",
  "O",
  "WA",
  "WAE",
  "OE",
  "YO",
  "U",
  "WEO",
  "WE",
  "WI",
  "YU",
  "EU",
  "YI",
  "I",
];
const finalConsonants = [
  "",
  "G",
  "KK",
  "GS",
  "N",
  "NJ",
  "NH",
  "D",
  "L",
  "LG",
  "LM",
  "LB",
  "LS",
  "LT",
  "LP",
  "LH",
  "M",
  "B",
  "BS",
  "S",
  "SS",
  "NG",
  "J",
  "CH",
  "K",
  "T",
  "P",
  "H",
];

export const koreanToRoman = (korean: string) => {
  let result = "";

  for (let char of korean) {
    const code = char.charCodeAt(0);

    if (code >= 0xac00 && code <= 0xd7a3) {
      const syllableIndex = code - 0xac00;
      const initialIndex = Math.floor(syllableIndex / (21 * 28));
      const medialIndex = Math.floor((syllableIndex % (21 * 28)) / 28);
      const finalIndex = syllableIndex % 28;

      result +=
        initialConsonants[initialIndex] +
        medialVowels[medialIndex] +
        finalConsonants[finalIndex];
    } else {
      result += char;
    }
  }

  return result;
};
