import type { Plugin } from "esbuild";
import { readFile } from "node:fs/promises";
import * as path from "node:path";

export function htmlTemplatePlugin(): Plugin {
    return {
        name: "html-template",

        setup(build) {
            build.onResolve(
                { filter: /\.html(?:\?raw)?$/ },
                (args) => ({
                    path: path.resolve(
                        args.resolveDir,
                        args.path.replace(/\?raw$/, ""),
                    ),
                    namespace: "html-template",
                }),
            );

            build.onLoad(
                {
                    filter: /\.html$/,
                    namespace: "html-template",
                },
                async (args) => ({
                    contents: `export default ${JSON.stringify(
                        await readFile(args.path, "utf8"),
                    )};`,
                    loader: "js",
                }),
            );
        },
    };
}