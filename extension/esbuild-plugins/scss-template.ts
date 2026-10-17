import type { Plugin } from "esbuild";
import * as path from "node:path";
import { compile } from "sass";

export function scssTemplatePlugin(): Plugin {
    return {
        name: "scss-template",

        setup(build) {
            build.onResolve(
                { filter: /\.scss\?raw$/ },
                (args) => ({
                    path: path.resolve(
                        args.resolveDir,
                        args.path.replace(/\?raw$/, ""),
                    ),
                    namespace: "scss-template",
                }),
            );

            build.onLoad(
                {
                    filter: /\.scss$/,
                    namespace: "scss-template",
                },
                (args) => {
                    const result = compile(args.path);

                    return {
                        contents: `export default ${JSON.stringify(
                            result.css,
                        )};`,
                        loader: "js",
                    };
                },
            );
        },
    };
}