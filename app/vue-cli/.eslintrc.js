module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:prettier/recommended',
    'plugin:vue/vue3-recommended',
    '@vue/typescript/recommended',
    '@vue/prettier',
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  plugins: ['prettier', '@typescript-eslint'],
  rules: {
    'vue/multi-word-component-names': 0,
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
  },
  overrides: [
    {
      files: [
        '**/__tests__/*.{j,t}s?(x)',
        '**/tests/unit/**/*.spec.{j,t}s?(x)',
      ],
      env: {
        jest: true,
      },
    },
  ],
}
