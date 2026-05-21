import {renderVideo} from '@revideo/renderer';

async function render() {
  console.log('Rendering video...');
  const file = await renderVideo({
    projectFile: './src/project.tsx',
    settings: {
      logProgress: true,
      puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      },
    },
  });
  console.log(`Rendered video to ${file}`);
  process.exit(0);
}

render();
