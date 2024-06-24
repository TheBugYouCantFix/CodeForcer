import styled, { css } from "styled-components";

const StyledLabel = styled.label`
  position: relative;
  padding-top: 2.7rem;

  & > input,
  & > label > span {
    padding-top: 1.3rem;
    padding-bottom: 1.3rem;
  }
  & > input {
    width: 100%;
  }
  & > input + input {
    margin-top: 1.4rem;
  }
  &:not(:last-child) {
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--color-grey-100);
  }
  input:focus ~ span {
    transform: translate(1rem, -1.6rem) scale(1.2);
  }

  ${(props) =>
    props.type === "file" &&
    css`
      &:hover > span {
        transform: translate(1rem, -1.6rem) scale(1.2);
      }
    `}
`;
const StyledSpan = styled.span`
  position: absolute;
  top: 1.6rem;
  left: 1rem;
  padding: 0 1rem 0 0.2rem;
  background-color: var(--color-grey-0);
  border-radius: var(--border-radius-md);

  font-size: 1.5rem;
  transition: transform 0.3s ease;
`;

function FormElement({ label, children, type = "" }) {
  return (
    <StyledLabel type={type}>
      {children}
      <StyledSpan>{label}</StyledSpan>
    </StyledLabel>
  );
}

export default FormElement;
