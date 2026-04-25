import { DemoProductShell } from "@/components/demo/demo-product-shell";

export default function DemoLayout({ children }: { children: React.ReactNode }) {
  return <DemoProductShell>{children}</DemoProductShell>;
}
