import { Outlet, useNavigation } from "react-router-dom";
import styled from "styled-components";
import Sidebar from "./Sidebar.jsx";
import FullPage from "./FullPage.jsx";
import Spinner from "./Spinner.jsx";

const StyledAppLayout = styled.div`
  display: grid;
  grid-template-columns: 28rem 1fr;
  // grid-template-rows: auto 1fr;
  height: 100dvh;
`;
const Main = styled.main`
  position: relative;
  background-color: var(--color-grey-50);
  padding: 4rem 4.8rem 6.4rem;
  overflow-y: auto;
  transition: opacity 0.5s ease;
`;

const Container = styled.div`
  min-height: 100%;
  max-width: 120rem;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3.2rem;
`;

function AppLayout() {
  const navigation = useNavigation();
  return (
    <StyledAppLayout>
      <Sidebar />
      <Main>
        {navigation.state === "loading" && (
          <FullPage>
            <Spinner />
          </FullPage>
        )}
        <Container>
          <Outlet />
        </Container>
      </Main>
    </StyledAppLayout>
  );
}

export default AppLayout;
