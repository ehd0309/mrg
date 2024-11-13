import { defineConfig } from "tsup";

export default defineConfig({
  clean: true,
  target: "es2020",
  entry: ["src"],
  format: ["cjs"],
  dts: true,
});
