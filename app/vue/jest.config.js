module.exports = {
  transform: {
    '^.+\\.tsx?$': [
      'ts-jest',
      {
        babel: true,
        tsConfig: 'tsconfig.json',
      },
    ],
  },
  preset: 'ts-jest',
}
