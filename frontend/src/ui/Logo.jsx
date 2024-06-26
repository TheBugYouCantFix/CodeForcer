import styled from "styled-components";

const StyledLogo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.05rem;
`;

const Img = styled.img`
  flex: 0 0 6.2rem;
  width: 6.2rem;
  height: 6.2rem;
`;
const LogoText = styled.span`
  font-weight: 500;
  font-size: 2.4rem;
  line-height: 1.2;
  letter-spacing: 0.03em;
`;

function Logo() {
  return (
    <StyledLogo>
      <Img src={"./logo.svg"} alt="The logo of out application" />
      <LogoText>CodeForcer</LogoText>
    </StyledLogo>
  );
}

export default Logo;
