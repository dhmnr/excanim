import { exportToSvg } from "@excalidraw/excalidraw";

window.renderToSvg = async function (elements, appState, files) {
  const svg = await exportToSvg({
    elements,
    appState: Object.assign(
      {
        exportWithDarkMode: false,
        exportBackground: true,
        viewBackgroundColor: "#ffffff",
      },
      appState || {},
    ),
    files: files || {},
  });
  return svg.outerHTML;
};

window.bridgeReady = true;
