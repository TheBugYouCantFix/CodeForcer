import styled, { css } from "styled-components";
import Input from "../../ui/Input.jsx";

export const StyledCover = styled.div`
  position: relative;
  max-width: 90rem;
  gap: 1rem;

  text-align: center;
  color: var(--color-grey-600);
  font-size: 1.6rem;
  font-weight: 500;
  padding: 3rem 4.5rem 5rem;
  transition: all 0.3s;
  box-shadow: var(--shadow-md);
  border-radius: var(--border-radius-md);
`;

export const ButtonBack = styled.button`
  position: absolute;
  left: 2rem;
  top: 2rem;
  background-color: transparent;
  border: none;

  svg {
    width: 5rem;
    height: 5rem;
    transition: fill 0.3s ease;
  }
  &:hover svg {
    fill: var(--color-brand-600);
  }
`;

export const Description = styled.div`
  display: flex;
  justify-content: center;

  &:not(:last-child) {
    margin-bottom: 3.5rem;
  }
`;

export const List = styled.form`
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3rem;

  button {
    align-self: center;
    padding-left: 8rem;
    padding-right: 8rem;
  }
`;
export const Item = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 3rem 4rem;
  column-gap: 0.8rem;
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-grey-100);

  font-weight: 400;

  strong {
    font-weight: 500;
  }

  > strong {
    font-size: 2rem;
  }
  > strong:not(:last-child) {
    margin-bottom: 1.5rem;
  }
  > input:not(:last-child) {
    margin-bottom: 0.2rem;
  }

  ${(props) =>
    parseInt(props.undefined) > 0 &&
    css`
      border: 1px solid var(--color-yellow-700);
    `}
`;

export const ItemRow = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.5rem;
  margin-top: 2rem;

  span {
    display: inline-flex;
    align-items: center;
    gap: 1rem;
  }
  span strong {
    align-self: flex-start;
    font-size: 2rem;
    padding-bottom: 0.3rem;
  }
`;

export const ItemInput = styled(Input)`
  max-width: 20rem;
  margin: 0 auto;
  text-align: center;
  padding: 0.3rem 1rem;
  font-size: 1.4rem;

  &:not(:last-child) {
    margin-bottom: 0.5rem;
  }
`;

export const Error = styled.span`
  font-size: 1.4rem;
  color: var(--color-red-700);
`;

export const UndefinedUsersList = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  row-gap: 0.6rem;
  column-gap: 1.2rem;
  margin-top: 2rem;

  & span {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
  }
  & span::before {
    content: "";
    flex: 0 0 0.3rem;
    width: 0.3rem;
    height: 0.3rem;
    border-radius: 100%;
    background-color: var(--color-grey-700);
  }
`;

export const UndefinedDescription = styled.p`
  padding: 2rem 2.5rem;
  border: 2px solid var(--color-red-400);
  border-radius: var(--border-radius-md);

  font-weight: 400;
  b {
    font-weight: 500;
  }
  a {
    font-weight: 500;
    text-decoration: underline;
  }
`;
