import { Toaster } from "react-hot-toast";
import GlobalStyles from "./styles/GlobalStyles.js";
import {
  BrowserRouter,
  createBrowserRouter,
  Route,
  RouterProvider,
  Routes,
} from "react-router-dom";
import AppLayout from "./ui/AppLayout.jsx";
import Home from "./pages/Home.jsx";
import Handles from "./pages/Handles.jsx";
import PageNotFound from "./pages/PageNotFound.jsx";
import Submissions from "./pages/Submissions.jsx";
import { DarkModeProvider } from "./context/DarkModeContext.jsx";
import Settings from "./pages/Setting.jsx";
import { ErrorBoundary } from "react-error-boundary";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    errorElement: <PageNotFound />,
    children: [
      {
        errorElement: <ErrorBoundary />,
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
      <Toaster
        position="top-center"
        reverseOrder={true}
        gutter={12}
        containerStyle={{ margin: "8px" }}
        toastOptions={{
          success: {
            duration: 3000,
          },
          error: {
            duration: 5000,
          },
          style: {
            fontSize: "1.6rem",
            maxWidth: "50rem",
            padding: "1.6rem 2.4rem",
            backgroundColor: "var(--color-grey-0)",
            color: "var(--color-grey-700)",
          },
        }}
      />
    </DarkModeProvider>
  );
}

export default App;
