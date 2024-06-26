import styled from "styled-components";
import Logo from "./Logo.jsx";
import MainNav from "./MainNav.jsx";
import ThemeButton from "./ThemeButton.jsx";

const StyledSwitch = styled(ThemeButton)`
  max-width: none;
`;

const StyledSidebar = styled.aside`
  grid-row: 1 / -1;
  display: flex;
  flex-direction: column;
  gap: 3.2rem;
  padding: 3.2rem 2.4rem;
  border-right: 1px solid var(--color-grey-100);
  background-color: var(--color-grey-0);
  overflow-y: auto;
`;

function Sidebar() {
  return (
    <StyledSidebar>
      <Logo />
      <MainNav />
      <StyledSwitch align={"center"} />
    </StyledSidebar>
  );
}

export default Sidebar;
