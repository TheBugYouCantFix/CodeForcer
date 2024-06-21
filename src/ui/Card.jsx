import styled from "styled-components";

const StyledCard = styled.a`
  display: flex;
  flex-direction: column;
  border-radius: var(--border-radius-sm);
  background-color: var(--color-grey-100);
`;

function Card({ children }) {
  return <StyledCard>{children}</StyledCard>;
}

export default Card;
