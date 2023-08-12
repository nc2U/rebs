import { Config } from 'jest'

const config: Config = {
  preset: '@vue/cli-plugin-unit-jest/presets/typescript-and-babel',
  // moduleFileExtensions: ['js', 'json', 'ts'],
  // modulePaths: ['<rootDir>'],
  // moduleDirectories: ['node_modules'],
  // testRegex: '.*\\.spec\\.ts$',
  transform: {
    '^.*\\.tsx?$': [
      'ts-jest',
      {
        babel: true,
        tsconfig: 'tsconfig.json',
      },
    ],
  },
  // // collectCoverageFrom: ['**/*.(t|j)s'],
  testEnvironment: 'node',
}

export default config
