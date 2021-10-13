module.exports = {
    root: true,
    env: {
        browser: true,
        commonjs: true,
        es2020: true,
        node: true,
    },
    extends: [
        "eslint:recommended",
        "plugin:vue/vue3-recommended",
    ],
    parser: "vue-eslint-parser",
    parserOptions: {
        parser: "@babel/eslint-parser",
        sourceType: "module",
        requireConfigFile: false,
    },
    rules: {
        "linebreak-style": ["error", "unix"],
        "camelcase": ["warn", {
            "properties": "never",
            "ignoreImports": true
        }],
        // override/add rules settings here, such as:
        // 'vue/no-unused-vars': 'error'
        "no-unused-vars": "warn",
        indent: [
            "error",
            4,
            {
                ignoredNodes: ["TemplateLiteral"],
                SwitchCase: 1,
            },
        ],
        quotes: ["warn", "double"],
        semi: "warn",
        "vue/html-indent": ["warn", 4], // default: 2
        "vue/max-attributes-per-line": "off",
        "vue/singleline-html-element-content-newline": "off",
        "vue/html-self-closing": "off",
        "vue/attribute-hyphenation": "off",     // This change noNL to "no-n-l" unexpectedly
        "no-multi-spaces": ["error", {
            ignoreEOLComments: true,
        }],
        "space-before-function-paren": ["error", {
            "anonymous": "always",
            "named": "never",
            "asyncArrow": "always"
        }],
        "curly": "error",
        "object-curly-spacing": ["error", "always"],
        "object-curly-newline": "off",
        "object-property-newline": "error",
        "comma-spacing": "error",
        "brace-style": "error",
        "no-var": "error",
        "key-spacing": "warn",
        "keyword-spacing": "warn",
        "space-infix-ops": "warn",
        "arrow-spacing": "warn",
        "no-trailing-spaces": "warn",
        "no-constant-condition": ["error", {
            "checkLoops": false,
        }],
        "space-before-blocks": "warn",
        //'no-console': 'warn',
        "no-extra-boolean-cast": "off",
        "no-multiple-empty-lines": ["warn", {
            "max": 1,
            "maxBOF": 0,
        }],
        "lines-between-class-members": ["warn", "always", {
            exceptAfterSingleLine: true,
        }],
        "no-unneeded-ternary": "error",
        "array-bracket-newline": ["error", "consistent"],
        "eol-last": ["error", "always"],
        //'prefer-template': 'error',
        "comma-dangle": ["warn", "only-multiline"],
        "no-empty": ["error", {
            "allowEmptyCatch": true
        }],
        "no-control-regex": "off",
        "one-var": ["error", "never"],
        "max-statements-per-line": ["error", { "max": 1 }]
    },
    "overrides": [
        {
            "files": [ "src/languages/*.js", "src/icon.js" ],
            "rules": {
                "comma-dangle": ["error", "always-multiline"],
            }
        },

        // Override for jest puppeteer
        {
            "files": [
                "**/*.spec.js",
                "**/*.spec.jsx"
            ],
            env: {
                jest: true,
            },
            globals: {
                page: true,
                browser: true,
                context: true,
                jestPuppeteer: true,
            },
        }
    ]
};
