import esbuild from "esbuild";
import { htmlTemplatePlugin } from "./esbuild-plugins/html-template.ts";
import { scssTemplatePlugin } from "./esbuild-plugins/scss-template.ts";

await esbuild.build({
    entryPoints: ["src/content-script.ts"],
    bundle: true,
    outfile: "dist/content-script.js",
    platform: "browser",
    format: "iife",
    plugins: [
        htmlTemplatePlugin(),
        scssTemplatePlugin(),
    ],
});