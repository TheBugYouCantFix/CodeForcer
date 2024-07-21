import styled, { css } from "styled-components";

const Input = styled.input`
  border: 1px solid var(--color-grey-300);
  border-radius: var(--border-radius-sm);
  padding: 0.8rem 1.2rem;
  background-color: var(--color-grey-0);
  box-shadow: var(--shadow-sm);

  ${(props) =>
    props?.error &&
    css`
      border-color: var(--color-red-400);

      &:focus {
        outline-color: var(--color-red-400);
      }
    `}
`;

export default Input;
