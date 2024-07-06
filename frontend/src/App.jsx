import GlobalStyles from "./styles/GlobalStyles.js";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import AppLayout from "./ui/AppLayout.jsx";
import Home from "./pages/Home.jsx";
import Handles from "./pages/Handles.jsx";
import PageNotFound from "./pages/PageNotFound.jsx";
import Submissions from "./pages/Submissions.jsx";
import { DarkModeProvider } from "./context/DarkModeContext.jsx";
import Settings, { loader as settingsLoader } from "./pages/Setting.jsx";
import ErrorFallback from "./ui/ErrorFallback.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    errorElement: <PageNotFound />,
    children: [
      {
        errorElement: <ErrorFallback />,
        children: [
          {
            index: true,
            element: <Home />,
          },
          {
            path: "handles",
            element: <Handles />,
          },
          {
            path: "submissions",
            element: <Submissions />,
          },
          {
            path: "submissions/:contestId",
            element: <Settings />,
            loader: settingsLoader,
          },
        ],
      },
    ],
  },
]);

function App() {
  return (
    <DarkModeProvider>
      <GlobalStyles />
      <RouterProvider router={router} />
    </DarkModeProvider>
  );
}

export default App;
