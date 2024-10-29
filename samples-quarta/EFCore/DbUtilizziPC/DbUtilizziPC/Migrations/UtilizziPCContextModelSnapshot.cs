﻿// <auto-generated />
using System;
using DbUtilizziPC.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

#nullable disable

namespace DbUtilizziPC.Migrations
{
    [DbContext(typeof(UtilizziPCContext))]
    partial class UtilizziPCContextModelSnapshot : ModelSnapshot
    {
        protected override void BuildModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder.HasAnnotation("ProductVersion", "8.0.10");

            modelBuilder.Entity("DbUtilizziPC.Model.Classe", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("Aula")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("Nome")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.HasKey("Id");

                    b.HasIndex("Nome")
                        .IsUnique();

                    b.ToTable("Classi");
                });

            modelBuilder.Entity("DbUtilizziPC.Model.Computer", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("Collocazione")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("Modello")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.HasKey("Id");

                    b.ToTable("Computers");
                });

            modelBuilder.Entity("DbUtilizziPC.Model.Studente", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<int>("ClasseId")
                        .HasColumnType("INTEGER");

                    b.Property<string>("Cognome")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("Nome")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.HasKey("Id");

                    b.HasIndex("ClasseId");

                    b.ToTable("Studenti");
                });

            modelBuilder.Entity("DbUtilizziPC.Model.Utilizza", b =>
                {
                    b.Property<int>("StudenteId")
                        .HasColumnType("INTEGER");

                    b.Property<int>("ComputerId")
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("DataOraInizioUtilizzo")
                        .HasColumnType("TEXT");

                    b.Property<DateTime?>("DataOraFineUtilizzo")
                        .HasColumnType("TEXT");

                    b.HasKey("StudenteId", "ComputerId", "DataOraInizioUtilizzo");

                    b.HasIndex("ComputerId");

                    b.ToTable("Utilizzi");
                });

            modelBuilder.Entity("DbUtilizziPC.Model.Studente", b =>
                {
                    b.HasOne("DbUtilizziPC.Model.Classe", "Classe")
                        .WithMany("Studenti")
                        .HasForeignKey("ClasseId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Classe");
                });

            modelBuilder.Entity("DbUtilizziPC.Model.Utilizza", b =>
                {
                    b.HasOne("DbUtilizziPC.Model.Computer", "Computer")
                        .WithMany("Utilizzi")
                        .HasForeignKey("ComputerId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("DbUtilizziPC.Model.Studente", "Studente")
                        .WithMany("Utilizzi")
                        .HasForeignKey("StudenteId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Computer");

                    b.Navigation("Studente");
                });

            modelBuilder.Entity("DbUtilizziPC.Model.Classe", b =>
                {
                    b.Navigation("Studenti");
                });

            modelBuilder.Entity("DbUtilizziPC.Model.Computer", b =>
                {
                    b.Navigation("Utilizzi");
                });

            modelBuilder.Entity("DbUtilizziPC.Model.Studente", b =>
                {
                    b.Navigation("Utilizzi");
                });
#pragma warning restore 612, 618
        }
    }
}
